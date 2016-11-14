#!/usr/bin/env python
#
#  This implements the website logic, this is where you would do any dynamic
#  programming for the site pages and render them from templaes.
#
#  NOTE: This file will need heavy customizations.  Search for "XXX".
#
#  See the README.md for more information
#
#  Written by Sean Reifschneider <jafo@jafo.ca>, 2013
#
#  Part of the python-bottle-skeleton project at:
#
#      https://github.com/linsomniac/python-bottle-skeleton
#
#  I hereby place this work, python-bottle-wrapper, into the public domain.

#  XXX Remove these two lines if you aren't using a database
from lib.bottledbwrap import dbwrap
import model
from bottle import template, abort
from bottle import (view, TEMPLATE_PATH, Bottle, static_file, request,
                    redirect, BaseTemplate)

#  XXX Remove these lines and the next section if you aren't processing forms
from wtforms import (Form, StringField, SelectField, FieldList, FormField,
                     PasswordField, validators, DateField, DateTimeField)

from wtforms.fields.html5 import (DecimalField)

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

import json


#  XXX Form validation example
class NewUserFormProcessor(Form):
    name = StringField('Username', [validators.Length(min=4, max=25)])
    full_name = StringField('Full Name', [validators.Length(min=4, max=60)])
    email_address = StringField(
        'Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField(
        'New Password',
        [validators.DataRequired(),
         validators.EqualTo('confirm',
                            message='Passwords must match')
         ])
    confirm = PasswordField('Repeat Password')


class PlageFormProcess(Form):
    heure = DateTimeField(None, [validators.Optional()],format="%H:%M" )
    temperature = DecimalField(None, [validators.Optional()])


class PlanningFormProcessor(Form):
    libelle = StringField('Libellé', [validators.Length(min=5, max=40)])
    plages = FieldList(FormField(PlageFormProcess), "plages", None, 5, 10)

class CyclePlanningFormProcessor(Form):
    #position = IntegerField('Position', [validators.Optional()])
    planning_id = SelectField('planning', coerce=int)

class CycleFormProcessor(Form):
    libelle = StringField('Libellé', [validators.Length(min=5, max=40)])
    plannings = FieldList(FormField(CyclePlanningFormProcessor), "plannings", None, 5, 14)
    #plannings = FieldList(SelectField('planning', coerce=int), "plannings", None, 5, 14)


class AffectationCycleFormProcessor(Form):
    debut = DateField(None, [validators.Optional()], format="%d/%m/%Y")
    fin = DateField(None, [validators.Optional()], format="%d/%m/%Y")
    cycle_id=SelectField('cycle', coerce=int)


def build_application():
    #  XXX Define application routes in this class

    app = Bottle()

    #  Pretty much this entire function needs to be written for your

    BaseTemplate.defaults['app'] = app  # XXX Template global variable
    TEMPLATE_PATH.insert(0, 'views')  # XXX Location of HTML templates

    #  XXX Routes to static content
    @app.route('/<path:re:favicon.ico>')
    @app.route('/static/<path:path>')
    def static(path):
        'Serve static content.'
        return static_file(path, root='static/')

    #  XXX Index page
    @app.route('/', name='index')  # XXX URL to page
    @view('index')  # XXX Name of template
    def index():
        'A simple form that shows the date'

        import datetime

        now = datetime.datetime.now()

        #  any local variables can be used in the template
        return locals()


        #  XXX Index page

    @app.route('/index2', name='index2')  # XXX URL to page
    @view('index2')  # XXX Name of template
    def index():
        'A simple form that shows the date'

        import datetime

        now = datetime.datetime.now()

        #  any local variables can be used in the template
        return locals()

    #  XXX User list page
    @app.route('/users', name='user_list')  # XXX URL to page
    @view('users')  # XXX Name of template
    def user_list():
        'A simple page from a dabase.'

        db = dbwrap.session()

        users = db.query(model.User).order_by(model.User.name)

        #  any local variables can be used in the template
        return locals()

    #  XXX User details dynamically-generated URL
    @app.route('/users/<username>', name='user')  # XXX URL to page
    @view('user')  # XXX Name of template
    def user_info(username):
        'A simple page from a dabase.'

        user = model.user_by_name(username)

        #  any local variables can be used in the template
        return locals()

    #  XXX A simple form example, not used on the demo site
    @app.route('/form')  # XXX URL to page
    @view('form')  # XXX Name of template
    def static_form():
        'A simple form processing example'

        form = NewUserFormProcessor(request.forms.decode())
        if request.method == 'POST' and form.validate():
            #  XXX Do something with form fields here

            #  if successful
            redirect('/users/%s' % form.name.data)

        # any local variables can be used in the template
        return locals()

    #  XXX Create a new user, form processing, including GET and POST
    @app.get('/new-user', name='user_new')  # XXX GET URL to page
    @app.post('/new-user')  # XXX POST URL to page
    @view('user-new')  # XXX Name of template
    def new_user():
        'A sample of interacting with a form and a database.'

        form = NewUserFormProcessor(request.forms.decode())

        if request.method == 'POST' and form.validate():
            db = dbwrap.session()

            sean = model.User(
                full_name=form.full_name.data, name=form.name.data,
                email_address=form.email_address.data)
            db.add(sean)
            db.commit()

            redirect(app.get_url('user', username=form.name.data))

        # any local variables can be used in the template
        return locals()

    @app.get('/edit_user/<username>', name='edit_user')  # XXX URL to page
    @app.post('/edit_user/<username>')  # XXX POST URL to page
    @view('user-new')
    def edit_user(username):
        user = model.user_by_name(username)
        form = NewUserFormProcessor(request.POST, user)

        if request.method == 'POST' and form.validate():
            db = dbwrap.session()
            form.populate_obj(user)
            print(user)
            db.merge(user)
            db.commit()

            redirect(app.get_url('user_list'))
        return locals()

    @app.get('/delete_user/<username>', name='delete_user')  # XXX POST URL to page
    def edit_user(username):
        db = dbwrap.session()
        user = db.query(model.User).filter_by(name=username).first()

        db.delete(user)
        db.commit()

        redirect(app.get_url('user_list'))

    """
       Affectation de Cycles
    """
    @app.route('/affectation_cycles', name='affectation_cycles')  # XXX URL to page
    @view('affectation_cycles')  # XXX Name of template
    def affectation_cycles_list():
        db = dbwrap.session()
        affectation_cycles = db.query(model.AffectationCycle).order_by(model.AffectationCycle.debut)
        return locals()

    @app.get('/delete_affectation_cycle/<id>', name='delete_affectation_cycle')
    def delete_affectation_cycle(id):
        db = dbwrap.session()
        cycle = db.query(model.AffectationCycle).filter_by(affectation_id=id).one()

        db.delete(cycle)
        db.commit()

        redirect(app.get_url('affectation_cycles'))

    @app.get('/update_affectation_cycle/<id>', name='update_affectation_cycle')
    @app.post('/update_affectation_cycle/<id>')
    @view('addorupdate_affectation_cycle')
    def update_affectation_cycle(id):
        db = dbwrap.session()

        affectationcycle = db.query(model.AffectationCycle).filter_by(affectation_id=id).one()
        form = AffectationCycleFormProcessor(request.forms.decode('utf-8'), affectationcycle)

        # peupler la combo de sélection des plannings
        cycles = [(cycle.cycle_id, cycle.libelle) for cycle in
                     db.query(model.Cycle).order_by('libelle')]
        form.cycle_id.choices = cycles
        form.cycle_id.default = form.cycle_id.data

        if request.method == 'POST' and form.validate():
            affectationcycle.debut= form.debut.data
            affectationcycle.fin = form.fin.data
            cycle = db.query(model.Cycle).filter_by(cycle_id=form.cycle_id.data).one()
            affectationcycle.cycle = cycle
            db.merge(affectationcycle)
            db.commit()
            redirect(app.get_url('affectation_cycles'))

        return  locals()

    @app.get('/new_affectation_cycle', name='new_affectation_cycle')
    @app.post('/new_affectation_cycle')  #
    @view('addorupdate_affectation_cycle')
    def new_affectation_cycle():
        db = dbwrap.session()

        form = AffectationCycleFormProcessor(request.forms.decode('utf-8'))

        # peupler la combo de sélection des plannings
        cycles = [(cycle.cycle_id, cycle.libelle) for cycle in
                  db.query(model.Cycle).order_by('libelle')]
        form.cycle_id.choices = cycles
        form.cycle_id.default = form.cycle_id.data

        if request.method == 'POST' and form.validate():

            affectationcycle = model.AffectationCycle()
            affectationcycle.debut = form.debut.data
            affectationcycle.fin = form.fin.data
            cycle = db.query(model.Cycle).filter_by(cycle_id=form.cycle_id.data).one()
            affectationcycle.cycle = cycle
            db.merge(affectationcycle)
            db.commit()
            redirect(app.get_url('affectation_cycles'))
        return locals()

    """
       Cycles
    """
    @app.route('/cycles', name='cycles')  # XXX URL to page
    @view('cycles')  # XXX Name of template
    def cycle_list():
        db = dbwrap.session()
        cycles = db.query(model.Cycle).order_by(model.Cycle.libelle)
        return locals()

    @app.get('/delete_cycle/<cycle_id>', name='delete_cycle')
    def delete_cycle(cycle_id):
        db = dbwrap.session()
        cycle = db.query(model.Cycle).filter_by(cycle_id=cycle_id).one()

        db.delete(cycle)
        db.commit()

        redirect(app.get_url('cycles'))

    @app.get('/update_cycle/<id>', name='update_cycle')
    @app.post('/update_cycle/<id>')
    @view('addorupdate_cycle')
    def update_cycle(id):
        db = dbwrap.session()

        cycle = db.query(model.Cycle).filter_by(cycle_id=id).one()
        form = CycleFormProcessor(request.forms.decode('utf-8'), cycle)

        # peupler la combo de sélection des plannings
        plannings = [(planning.planning_id, planning.libelle) for planning in
                     db.query(model.PlanningJour).order_by('libelle')]
        for planningForm in form.plannings:
            planningForm.planning_id.choices = plannings
            planningForm.planning_id.default = planningForm.planning_id.data

        if request.method == 'POST' and form.validate():
            cycle.libelle = form.libelle.data
            cycle.plannings = []
            #db.flush()
            position = 1
            for planningForm in form.plannings.data:
                planning = db.query(model.PlanningJour).filter_by(planning_id=planningForm['planning_id']).one()
                cycle.plannings.append( model.CyclePlanning(position=position, planning=planning))
                position = position+1
            db.merge(cycle)
            db.commit()

            redirect(app.get_url('cycles'))

        return locals()

    @app.get('/new_cycle', name='new_cycle')
    @app.post('/new_cycle')  #
    @view('addorupdate_cycle')  # XXX Name of template
    def new_cycle():
        'A sample of interacting with a form and a database.'

        db = dbwrap.session()
        form = CycleFormProcessor(request.forms.decode('utf-8'))

        plannings = [(planning.planning_id, planning.libelle) for planning in
                     db.query(model.PlanningJour).order_by('libelle')]
        for planningForm in form.plannings:
            planningForm.planning_id.choices = plannings

        if request.method == 'POST' and form.validate():
            cycle = model.Cycle(libelle=form.libelle.data)
            position = 1
            for planningForm in form.plannings.data:
                planning = db.query(model.PlanningJour).filter_by(planning_id=planningForm['planning_id']).one()
                cycle.plannings.append(model.CyclePlanning(position=position, planning=planning))
                position = position + 1
            db.add(cycle)
            db.commit()
            redirect(app.get_url('cycles'))

        # any local variables can be used in the template
        return locals()


    """
    Plannings jours
    """
    @app.route('/plannings', name='plannings')  # XXX URL to page
    @view('plannings')  # XXX Name of template
    def planning_jour_list():
        db = dbwrap.session()
        plannings = db.query(model.PlanningJour).order_by(model.PlanningJour.libelle)

        return locals()

    @app.get('/delete_planning/<planning_id>', name='delete_planning')
    def delete_planning(planning_id):
        db = dbwrap.session()
        planning = db.query(model.PlanningJour).filter_by(planning_id=planning_id).one()

        db.delete(planning)
        db.commit()

        redirect(app.get_url('plannings'))

    @app.get('/update_planning/<id>', name='update_planning')
    @app.post('/update_planning/<id>')
    @view('addorupdate_planning')
    def update_planning(id):
        db = dbwrap.session()
        planning = db.query(model.PlanningJour).filter_by(planning_id=id).first()

        form = PlanningFormProcessor(request.forms.decode('utf-8'), planning)


        if request.method == 'POST' and form.validate():
            planning.libelle = form.libelle.data
            planning.plages = []
            for plage in form.plages.data:
                if plage['heure'] is not None and plage['temperature'] is not None:
                    planning.plages.append(model.Plage(heure=plage['heure'], temperature=plage['temperature']))

            db.merge(planning)
            db.commit()

            redirect(app.get_url('plannings'))
        return locals()


    @app.get('/new_planning', name='new_planning')
    @app.post('/new_planning')  #
    @view('addorupdate_planning')  # XXX Name of template
    def new_planning():
        'A sample of interacting with a form and a database.'

        form = PlanningFormProcessor(request.forms.decode('utf-8'))
        if request.method == 'POST' and form.validate():
            db = dbwrap.session()

            planning = model.PlanningJour(libelle=form.libelle.data)

            for plageForm in form.plages.data:
                plage = model.Plage(heure=plageForm['heure'], temperature=plageForm['temperature'])
                if plage.heure is not None and plage.temperature is not None:
                    planning.plages.append(plage)

            db.add(planning)
            db.commit()

            redirect(app.get_url('plannings'))

        # any local variables can be used in the template
        return locals()


    test_dic = {
        'protocol': ['protocol1', 'protocol2', 'protocol3'],
        'service': ['s1', 's2', 's3'],
        'plugin': ['plug1', 'plug2', 'plug3'],
        'run': [1, 0, 1]
    }

    number_of_test_cases = len(test_dic['run'])

    @app.route('/page1')
    def serve_homepage():
        return template('disp_table', rows=test_dic, cases=number_of_test_cases, edit='service', check='run')

    @app.route('/new')
    def add_new():
        return template('add_case')

    @app.route('/new', method='POST')
    def add_new():
        for p in request.forms.getall('myTextEditBox'):
            print('p=', p)
        with open('test.json', 'w') as f:
            json.dump(test_dic, f)

    #  REQUIRED: return the application handle herre
    return app
