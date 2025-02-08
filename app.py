#####################################
## Credits: Giovanni Gaetani Liseo ##
#####################################

from flask import Flask, render_template, jsonify
from pysnmp.hlapi import *
from flask import Response
import json
import time

app = Flask(__name__)

# Classe RX-SAT
class Rx_sat:
    def __init__(self, id, postazione, indirizzo_ip, servizio, rt):
        self.id = id
        self.postazione = postazione
        self.indirizzo_ip = indirizzo_ip
        self.servizio = servizio
        self.rt = rt
        self.oids_rx_sat = { }

    @classmethod
    def create_rx_sat(cls, rx_sat_data):
        rx_sat_list = []
        for data in rx_sat_data:
            rx = cls(
                id=data[0],
                postazione=data[1], 
                indirizzo_ip=data[2], 
                servizio=data[3],
                rt=data[4]
            )
            rx_sat_list.append(rx)
        return rx_sat_list
    
    def scan_snmp_apparato(self):
        results = {}  # Inizializzo il dizionario dei risultati
        # Per ciascun OID
        for oid_name, oid_info in self.oids_rx_sat.items():
            oid = oid_info[0]
            moltiplicatore = oid_info[1]

            # Invio della richiesta SNMP
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(
                    getCmd(
                        SnmpEngine(),
                        CommunityData("public", mpModel=0),
                        UdpTransportTarget((self.indirizzo_ip, 161), timeout=1, retries=0),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid))
                    )
                )
            except Exception as e:
                results[oid_name] = "Errore"
                continue

            if errorIndication or errorStatus:
                results[oid_name] = "Errore"
                continue

            # Ottenimento del valore dall'SNMP
            
            valore_snmp = varBinds[0][1].prettyPrint()
            results[oid_name] = valore_snmp
            
        return results    


# Dati di esempio
rx_sat_data = []   

# Creazione istanza
rx_sat_list = Rx_sat.create_rx_sat(rx_sat_data)


@app.route('/')
def index():
    return render_template('sinottico.html', rx_sat_list=rx_sat_list)


@app.route('/stream')
def stream():
    def generate():
        while True:
            snmp_data = {}
            for rx in rx_sat_list:
                try:
                    snmp_data[rx.id] = rx.scan_snmp_apparato()
                    
                    # Invia i dati al client tramite SSE 
                    yield f"data: {json.dumps({rx.id: snmp_data[rx.id]})}\n\n"
                except Exception as e:
                    print(f"Errore durante la lettura SNMP per RX {rx.id}: {e}")
                # Piccola pausa tra le letture di ogni apparato
                time.sleep(0.1)
            # Pausa prima del prossimo ciclo completo
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)
