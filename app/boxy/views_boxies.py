from flask import render_template, redirect, request, url_for, flash, session, jsonify
from flask_login import login_required, current_user
from . import boxy
from ..models import Boxy
from .. import db
from app import states
from .forms_boxy import RegistrationBoxy



# @boxy.route('/inicio/boxy')
# @login_required
# def home_boxy():
#     salas = [boxy.sala for boxy in current_user.boxies.all()]
#     #claves_boxies = [boxy.clave_boxy for boxy in current_user.boxies.all()]
#     return render_template('boxy/home_boxy.html', salas=salas)

# Inicio del menú de boxies donde se pasan las boxies del cliente respectivo:
@boxy.route('/inicio/boxy')
@login_required
def home_boxy():
    states.clave_boxy = None
    boxies = [{"sala": boxy.sala, "clave": boxy.clave_boxy} for boxy in current_user.boxies.all()]
    return render_template('boxy/home_boxy.html', boxies=boxies)


# Endpoint para añadir una boxy desde el formulario enviado del cliente a la base de datos:
@boxy.route('/sumando_boxies', methods=['GET', 'POST'])
@login_required
def add_boxy():
    salas = [boxy.sala for boxy in current_user.boxies.all()]
    form = RegistrationBoxy()
    if form.validate_on_submit():
        new_boxy = Boxy(clave_boxy=form.clave_boxy.data,
                        sala = form.sala.data,
                        owner= current_user
                        )
        db.session.add(new_boxy)
        db.session.commit()
        flash('Boxy agregada con éxito!')
        return redirect(url_for('boxy.home_boxy'))
    return render_template('boxy/add_boxy.html', form=form, salas=salas)


# Se toma la clave de la boxy pedida por el cliente para obtener todos los datos de la base de datos.
# Posterior a eso se actualizan los datos para el protocolo MQTT:
@boxy.route('/control', methods = ['POST'])
@login_required
def control():
    #clave_of_boxy = request.args.get('clave')
    clave_of_boxy = request.form.get('clave')
    
    if not clave_of_boxy:
        return "No se envió clave", 400

    boxy = Boxy.query.filter_by(clave_boxy=clave_of_boxy).first()
    if not boxy:
        return "Boxy no encontrado", 404
    
    # guardar en el objeto states
    states.sala = boxy.sala
    states.clave_boxy = boxy.clave_boxy
    
    # ahora sala_seleccionada tiene el nombre de la sala elegida
    return render_template('boxy/controlando_salas.html', sala=boxy.sala)

   
    
@boxy.route('/api/ambiente', methods=['GET'])
@login_required
def api_ambiente():
    temperatura = states.temperatura if states.temperatura is not None else 0
    humedad = states.humedad if states.humedad is not None else 0
    return jsonify({"temp": temperatura, "hum": humedad})

@boxy.route('/api/accion', methods = ['GET', 'POST'])
@login_required
def api_action():
    data = request.get_json()
    states.actuator = data.get("accion")
    print(f"Acción recibida: {states.actuator}")
    # Aquí podés publicar por MQTT o guardar en DB
    return jsonify({"mensaje": f"Se envió la acción: {states.actuator}"})