import requests
import configparser
import json
import argparse

class APIClient:
    
    m_customer:str
    m_api:str
    m_api_key:str
    m_status:bool
    
    def __init__(self, api='unify', customer='default'):
        """
        Inicializa la clase APIClient.

        :param base_url: La URL base de la API.
        :param api_key: Clave de API para autenticación (opcional).
        :param headers: Encabezados personalizados para las solicitudes (opcional).
        """
        self.m_customer = customer
        self.m_api = api
        
        self.get_token()

    def get_token(self):
        if self.m_api == 'unify':

            payload = json.dumps(self.get_credentials())

            reqUrl = f"https://api.{self.m_customer}.bigfinite.ai/v2/token"

            headersList = {
                "Content-Type": "application/json" 
            }


        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
        
        if response.status_code in [200,203]:
            self.m_status = True
            data = response.json()
            self.m_api_key = data['accessToken']
            print('connected')
        else:
            self.m_status = False
            print(data['message'])

    def get_credentials(self) -> dict:
        # Crear un objeto ConfigParser
        config = configparser.ConfigParser(interpolation=None)

        # Leer el archivo de configuración
        config.read('/Users/alejandro.lopez.ext/.config/APIClient/apiClientCredentials.cfg')
        
        if self.m_api == 'unify':
            credentials = {
                'username': config[self.m_customer]['user'],
                'password': config[self.m_customer]['password'],
                'customer': config[self.m_customer]['customer']
            }
            
            self.m_customer = config[self.m_customer]['customer']
        
        return credentials
        
    def _make_request(self, method, endpoint, params=None, data=None, json=None):
        """
        Método interno para realizar solicitudes HTTP.

        :param method: Método HTTP (GET, POST, PUT, DELETE, etc.).
        :param endpoint: Endpoint de la API (relativo a la base_url).
        :param params: Parámetros de consulta para la solicitud (opcional).
        :param data: Datos en formato x-www-form-urlencoded o multipart (opcional).
        :param json: Datos en formato JSON (opcional).
        :return: Respuesta de la API.
        """
        
        headersList = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.m_api_key
            }
        
        try:
            response = requests.request(
                method=method,
                url=endpoint,
                headers=headersList,
                params=params,
                data=data,
                json=json
            )
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP
            return response.json()  # Devuelve el cuerpo de la respuesta en formato JSON
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None

    def get(self, entity_type, entity_id, endpoint, params=None):
        """Realiza una solicitud GET."""
        
        if self.m_api == 'unify':
            url = f"https://api.{self.m_customer}.bigfinite.ai/v2/{entity_type}/{entity_id}/{endpoint}"
        
        return self._make_request("GET", url, params=params)

    def post(self, endpoint, data=None, json=None):
        """Realiza una solicitud POST."""
        return self._make_request("POST", endpoint, data=data, json=json)

    def put(self, endpoint, data=None, json=None):
        """Realiza una solicitud PUT."""
        return self._make_request("PUT", endpoint, data=data, json=json)

    def delete(self, endpoint, params=None):
        """Realiza una solicitud DELETE."""
        return self._make_request("DELETE", endpoint, params=params)

if __name__ == "__main__":
    # Configurar argparse
    parser = argparse.ArgumentParser(description="API Client CLI")
    parser.add_argument("--api", required=True, help="API to connect")
    parser.add_argument("--customer", required=True, help="Customer")
    parser.add_argument("--method", required=True, help="Method")
    parser.add_argument("--entity_type", required=True, help="Type of Entity")
    parser.add_argument("--entity_id", required=True, help="ID of Entity")
    parser.add_argument("--endpoint", required=True, help="Endpoint")
    parser.add_argument("--startDate", required=False, help="Endpoint")
    parser.add_argument("--endDate", required=False, help="Endpoint")
    
    # Parsear argumentos
    args = parser.parse_args()

    # Crear instancia del cliente y obtener datos
    client = APIClient(api=args.api, customer=args.customer)
    
    if args.startDate == None and  args.endDate == None:
        params = {
            "startDate": "2024-11-19T00:01:55.000Z",
            "endDate": "2024-11-19T00:05:55.000Z"
        }
    else:
        params = {
            "startDate": args.startDate,
            "endDate": args.endDate
        }
    
    try:
        if args.method == "GET":
            data = client.get('elements','IPS_Base_flow_rate','values',params)
        print("Datos obtenidos de la API:", data)
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos: {e}")
