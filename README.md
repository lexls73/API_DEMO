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


   
2. GET VALUES: 
   python api_client.py --api "unify" --customer "appdev" --action "get" --endpoint "values" --entity_type "elements"  --entity_id "IPS_Base_flow_rate" --data_files "TRUE"
   CREATE ELEMENTS
   python api_client.py --api "unify" --customer "appdev" --action "create" --endpoint "elements"
   DELETE ELEMENTS
   python api_client.py --api "unify" --customer "appdev" --action "delete" --endpoint "elements"
   MASTER-RECIPIES
   python api_client.py --api "unify" --customer "appdev" --action "query" --endpoint "master-recipes" --entity_id "24050_1717579566"
3. 
4. 
5. Instalar venv: python -m venv .venv 
   Activar EV: source .venv/bin/activate
   Desactivar EV: deactivate