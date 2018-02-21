from zeep import Client

import settings


ResearchClient = Client(wsdl=settings.GENESIS_SERVICES['research'], strict=False)
ExportClient = Client(wsdl=settings.GENESIS_SERVICES['export'], strict=False)
