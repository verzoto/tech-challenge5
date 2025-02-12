# Tech Challenge 5

O objetivo deste projeto é utilizar Inteligencia Artificial para identificar objetos cortantes(facas, tesouras e similares) e emitir um alerta quando detectado.

## Dataset
[https://github.com/ari-dasci/OD-WeaponDetection/tree/master/Weapons%20and%20similar%20handled%20objects](https://github.com/ari-dasci/OD-WeaponDetection/tree/master/Weapons%20and%20similar%20handled%20objects)

## Pacotes utilizados
- [Django](https://www.djangoproject.com/)
- [Ultralytics YOLOv11](https://docs.ultralytics.com/pt/models/yolo11/)

## Como executar
1. Inicializar o ambiente virtual
   
   `python -m venv .`
2. Ativar o ambiente virtual
  
   `source bin/activate`
3. Instalar os pacotes necessários
  
   `pip install -r requirements.txt`


 4. Executar o serviço
   
    `python manage.py runserver`

5. Abrir a URL no navegador
  
   `http://localhost:8000/guardian/`

** Para funcionamento do envio de e-mail, é necessário configurar um SMTP no arquivo `.env` **