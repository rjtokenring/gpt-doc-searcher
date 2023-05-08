import os
import connexion
from connexion.resolver import RestyResolver

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger/', server='tornado')
    app.add_api('docsearch-microservice.yaml', resolver=RestyResolver('api'))
    app.run(port=int(os.environ.get('PORT', 9000)))
