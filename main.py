import json
import argparse
from api_client import APIClient

if __name__ == "__main__":
    # Configurar argparse
    parser = argparse.ArgumentParser(description="API Client CLI")
    parser.add_argument("--api", required=True, help="API to connect")
    parser.add_argument("--customer", required=True, help="Customer")
    parser.add_argument("--action", required=True, help=["get","create","update","delete","query"])
    parser.add_argument("--endpoint", required=False, help="Endpoint")
    parser.add_argument("--entity_type", required=False, help="Type of Entity")
    parser.add_argument("--entity_id", required=False, help="ID of Entity")
    parser.add_argument("--data_files", required=False, help="")

    # Parsear argumentos
    args = parser.parse_args()

    # Crear instancia del cliente y obtener datos
    client = APIClient(api=args.api, customer=args.customer)

    try:
        if args.action == "get":

            if args.api == 'execute':
                params = None
            else:
                with open("./PAYLOADS/params.json") as f:
                    params = json.load(f)

            files = True

            if args.data_files == "FALSE":
                files = False

            result = client.get(args.entity_type, args.entity_id, args.endpoint, params, files)

            if result:
                print("====================================")
                print("Datos obtenidos de la API y guardados.")
            else:
                print("====================================")
                print("Error al obtener los datos.")

        elif args.action == "query":

            with open("./PAYLOADS/master_recipie.json") as f:
                payload = json.dumps(json.load(f))

            result = client.post(
                endpoint=args.endpoint,
                entity_id=args.entity_id,
                data=payload,
                job_id=True,
            )

            if result:
                print("====================================")
                print("Query realizado. Datos en Archivo.")
            else:
                print("====================================")
                print(f"Error al realizar el query")

        elif args.action == "create" or args.action == "update":

            with open(f"./PAYLOADS/{args.action}.json") as f:
                payload = json.dumps(json.load(f))

            result = client.post(
                endpoint=args.endpoint,
                data=None, 
                json=payload
            )

            if result:
                print("====================================")
                print("Datos creados o actualizados.")
            else:
                print("====================================")
                print(f"Error al crear o actualizar la entidad")

        elif args.action == "delete":
            
            with open(f"./PAYLOADS/{args.action}.json") as f:
                id_arrays = json.load(f)
                
            data = json.dumps({
                "reason-of-request":"delete"
            })

            for val in id_arrays:
                result = client.delete(endpoint=args.endpoint,val=val,data=data)

                if result:
                    print("====================================")
                    print(f"Entidad {val} Borrados.")
                else:
                    print("====================================")
                    print(f"Error al borrar la entidad {val}")
                    
        elif args.action == "put":
            result = client.put(args.endpoint)
            if result:
                print("====================================")
            else:
                print("====================================")

        else:
            pass #TODO

    except Exception as e:
        print("============ERROR=============")
        print(f"Error al obtener datos: {e}")