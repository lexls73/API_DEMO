# Nombre del Proyecto

Breve descripción del proyecto y su propósito.

## Tabla de Contenidos
1. [Instalación](#instalación)
2. [Uso](#uso)
3. [Contribución](#contribución)
4. [Licencia](#licencia)
5. [Entorno virtual] 

## Instalación
1. Clona este repositorio:


   
2. UNIFY 
   GET VALUES: 
   python main.py --api "unify" --customer "appdev" --action "get" --endpoint "values" --entity_type "elements"  --entity_id "IPS_Base_flow_rate" --data_files "TRUE"
   CREATE ELEMENTS
   python main.py --api "unify" --customer "appdev" --action "create" --endpoint "elements"
   DELETE ELEMENTS
   python main.py --api "unify" --customer "appdev" --action "delete" --endpoint "elements"
   MASTER-RECIPIES
   python main.py --api "unify" --customer "appdev" --action "query" --endpoint "master-recipes" --entity_id "24050_1717579566"
   =========================================================================================================================================
   EXECUTE
   GET PO BY ID
   python main.py --api "execute" --customer "freseniuskabi-3" --action "get" --entity_type "process-orders" --entity_id "Wilson_NewPackaging_12345" --data_files "FALSE"
   GET STATUS
   python main.py --api "execute" --customer "freseniuskabi-3" --action "get" --endpoint "exec-status" --entity_type "process-orders" --entity_id "Wilson_NewPackaging_12345" --data_files "FALSE"
   GET RECORDS
   python main.py --api "execute" --customer "freseniuskabi-3" --action "get" --endpoint "records" --entity_type "process-orders" --entity_id "Wilson_NewPackaging_12345" --data_files "FALSE"

3. 
4. 
5. Instalar venv: python -m venv .venv 
   Activar EV: source .venv/bin/activate
   Desactivar EV: deactivate