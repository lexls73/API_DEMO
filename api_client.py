import requests
import configparser
import json
import pandas as pd
import os

class APIClient:

    m_customer: str
    m_api: str
    m_api_key: str
    m_status: bool
    m_archivo: str
    m_create_data: bool
    m_job_id: str
    m_mr_id: str
    M_FOLDER_PATH = "./DATA/"
    M_UNIFY_CREDENTIALS_PATH = (
        "/Users/alejandro.lopez.ext/.config/PlatformAPIClient/apiClientCredentials.cfg"
    )

    M_ALLOW_METHODS = ["GET", "POST", "DEL"]

    def __init__(self, api="unify", customer="default"):
        """
        Inicializa la clase APIClient.

        :param api: La API a la q se quiere conectar: unify o execute.
        :param customer: Environment al q se quiere conectar.
        """
        self.m_customer = customer.lower()
        self.m_api = api.lower()
        print("====================================")
        print("Iniciando la API")

        self.get_token()

    def get_token(self):
        if self.m_api == "unify":

            payload = json.dumps(self.get_credentials())

            print("====================================")
            print(f"Obteniendo el TOKEN para UNIFY - Customer {self.m_customer}")

            reqUrl = f"https://api.{self.m_customer}.bigfinite.ai/v2/token"

            headersList = {"Content-Type": "application/json"}

        response = requests.request("POST", reqUrl, data=payload, headers=headersList)

        if response.status_code in [200, 203]:
            self.m_status = True
            data = response.json()
            self.m_api_key = data["accessToken"]
            print("====================================")
            print("Conectado - token obtenido")
        else:
            self.m_status = False
            print("============ERROR=============")
            print(data["message"])

    def get_credentials(self) -> dict:
        # Crear un objeto ConfigParser
        config = configparser.ConfigParser(interpolation=None)

        if self.m_api == "unify":
            print("====================================")
            print(f"Obteniendo Credenciales para entorno {self.m_customer}")

            # Leer el archivo de configuración
            config.read(self.M_UNIFY_CREDENTIALS_PATH)

            credentials = {
                "username": config[self.m_customer]["user"],
                "password": config[self.m_customer]["password"],
                "customer": config[self.m_customer]["customer"],
            }

            self.m_customer = config[self.m_customer]["customer"]

            print("====================================")
            print(
                f"Credenciales para usuario {config[self.m_customer]['user']} Obtenidas"
            )
        else:
            print("====================================")
            print(f"Obteniendo Credenciales para entorno {self.m_customer}")

        return credentials

    def create_json(self, datos_json):

        print("====================================")
        print("Borrando archivos antiguos")
        for filename in os.listdir(self.M_FOLDER_PATH):
            file_path = os.path.join(self.M_FOLDER_PATH, filename)
            if os.path.isfile(file_path):  # Comprobar si es un archivo
                os.remove(file_path)  # Eliminar el archivo

        print("====================================")
        print("Archivos borrados")

        # Guardar el JSON en un archivo
        file = f"{self.M_FOLDER_PATH}{self.m_archivo}.json"
        with open(file, "w", encoding="utf-8") as archivo:
            json.dump(datos_json, archivo, ensure_ascii=False, indent=4)

        print("====================================")
        print("Archivo JSON Creado")

        if self.m_create_data:
            self.create_files(file)

    def create_files(self, file):

        df = pd.read_json(file)

        # file_sin_extension = file.replace(".json", "")

        df.to_excel(f"{self.M_FOLDER_PATH}{self.m_archivo}.xlsx", index=True)
        print("====================================")
        print("Archivo Excel Creado")
        df.to_csv(f"{self.M_FOLDER_PATH}{self.m_archivo}.csv", index=True)
        print("====================================")
        print("Archivo csv Creado")

    def _make_request(
        self, method, url, params=None, data=None, json=None, val="", job_id=False
    ) -> bool:
        """
        Método interno para realizar solicitudes HTTP.

        :param method: Método HTTP (GET, POST, PUT, DELETE, etc.).
        :param endpoint: Endpoint de la API (relativo a la base_url).
        :param params: Parámetros de consulta para la solicitud (opcional).
        :param data: Datos en formato x-www-form-urlencoded o multipart (opcional).
        :param json: Datos en formato JSON (opcional).
        :return bool: Respuesta de la API true o false.
        """

        if self.m_status:
            headersList = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.m_api_key,
            }
            if method in self.M_ALLOW_METHODS:
                try:
                    response = requests.request(
                        method=method,
                        url=url,
                        headers=headersList,
                        params=params,
                        data=data,
                        json=json,
                    )

                    response.raise_for_status()  # Lanza una excepción si hay un error HTTP

                    if job_id == True:
                        print("====================================")
                        print("Obteniendo el jobID")
                        self.m_job_id = response.json()["jobID"]
                        print("====================================")
                        print("Iterando en la paginación")
                        ret = self.get_job_id(self.m_job_id)
                        print("====================================")
                        print("Record query exitoso")
                        self.m_archivo = "record_query"
                        self.create_json(ret)
                    else:
                        if method == "GET":
                            self.create_json(response.json()["_embedded"]["items"])
                            print("====================================")
                            print("GET Exitoso")
                        elif method == "POST":
                            self.m_archivo = "prueba"
                            self.create_json(response.json())
                            print("====================================")
                            print("POST Exitoso")
                        elif method == "DEL":
                            print("====================================")
                            print(f"Entidad {val} borrada")
                    return True
                except requests.exceptions.RequestException as e:
                    print("============ERROR=============")
                    print(f"Error en la solicitud: {e}")
                    return False
            else:
                print("====================================")
                print(f"Metodo desconocido o no configurado. Metodos actualmente configurados {self.M_ALLOW_METHODS}")
                return False

    def get_job_id(self, jobID) -> list:

        headersList = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.m_api_key,
        }
        limit = 100  #Número de resultados por página
        offset = 0  #Índice inicial
        i=1

        records = []
        
        status = 'RUNNING'
        
        params = {"limit": limit, "offset": offset}
        
        while status != 'DONE':

            url = f"https://api.{self.m_customer}.bigfinite.ai/v2/master-recipes/{self.m_mr_id}/record-queries/{jobID}"
            response = requests.get(url, params=params, headers=headersList)
            response.raise_for_status()

            data = response.json()

            if 'status' in data:
                status = data['status']
                print("====================================")
                print(f"Estado del job id: {status}")
            else:
                status = 'DONE'
                print("====================================")
                print(f"Estado del job id: {status}")

        while True:
            print("====================================")
            print(f"Pagina: {i}")
            
            params = {"limit": limit, "offset": offset}

            url = f"https://api.{self.m_customer}.bigfinite.ai/v2/master-recipes/{self.m_mr_id}/record-queries/{jobID}"

            response = requests.get(url, params=params, headers=headersList)
            response.raise_for_status()

            data = response.json()
            
            if not data["records"]:  # Si la lista de resultados está vacía, terminamos
                print("====================================")
                print(f"Paginación terminada")
                break
            else:
                for val in data["records"]:
                    records.append(val)
            offset += limit
            i=i+1

        return records

    def get(self, entity_type, entity_id, endpoint, params=None, date_files=False):
        """Realiza una solicitud GET."""

        self.m_archivo = entity_id
        self.m_create_data = date_files
        if self.m_api == "unify":
            url = f"https://api.{self.m_customer}.bigfinite.ai/v2/{entity_type}/{entity_id}/{endpoint}"

        return self._make_request("GET", url, params=params)

    def post(self, endpoint, entity_id="", data=None, json=None, job_id=False):
        """Realiza una solicitud POST."""

        self.m_create_data = False
        if self.m_api == "unify":
            if entity_id != "":
                url = f"https://api.{self.m_customer}.bigfinite.ai/v2/{endpoint}/{entity_id}/record-queries"
                self.m_mr_id = entity_id
            else:
                url = f"https://api.{self.m_customer}.bigfinite.ai/v2/{endpoint}"

        else:
            pass

        return self._make_request("POST", url, data=data, json=json, job_id=job_id)

    def put(self, endpoint, data=None, json=None):
        """Realiza una solicitud PUT."""
        return self._make_request("PUT", endpoint, data=data, json=json)

    def delete(self, endpoint, val, params=None, data=None, json=None):
        """Realiza una solicitud DELETE."""
        self.m_create_data = False
        if self.m_api == "unify":
            url = f"https://api.{self.m_customer}.bigfinite.ai/v2/{endpoint}/{val}"
            return self._make_request(
                "DEL", url, params=params, data=data, json=json, val=val
            )



#client = APIClient(api="unify", customer="canary")

#with open("./PAYLOADS/master_recipie.json") as f:
#    payload = json.dumps(json.load(f))

#result = client.post(
#    endpoint="master-recipes",
#    entity_id="24050_1717579566",
#    data=payload,
#    job_id=True,
#)