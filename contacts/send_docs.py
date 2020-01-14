
import base64
import os
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document

# Settings
# Fill in these constants
#
# Obtain an OAuth access token from https://developers.docusign.com/oauth-token-generator
access_token = 'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQkAAAABAAUABwAAYQHXwQvXSAgAAKEk5QQM10gCAA0ub7zF2aNDkDF_jvUg2I4VAAEAAAAYAAkAAAAFAAAAKwAAAC0AAAAvAAAAMQAAADIAAAA4AAAAMwAAADUAAAANACQAAABmMGYyN2YwZS04NTdkLTRhNzEtYTRkYS0zMmNlY2FlM2E5NzgwAIBzwr_BC9dINwA_nANvB0-pSI_UFfRSxNre.5dxu946lX6nhNuk-0CUUH1IZ1jABZwBs8_vYQ6qspSNS9ELne4pISlQYtqayiS3Vx0jwqwc0PHh_bczMv_MD8O_P9mq6NLOk2lGniqrJWitiQJ-Y57QGWgcGfI-R0iSa54iv-LcqMSavOT-KVx3yB2YmCesw7c0aisr3FOBu2rJj1Xhiwz9uzenGk2mOWziJ17_S5WkQH1KwMofghWAA2LaB0qNqn81ccsYccdJhwV_LO8mu3c7uY36Eaxw14w-iRxctyMBNPOfjl3nubd_1cQmDcs-Py-OrLwrq24dHsKJQGdpd1W8uFXgggfW2Dw5emqSFLQ1KDvMZupnoorrkWw'
# Obtain your accountId from demo.docusign.com -- the account id is shown in the drop down on the
# upper right corner of the screen by your picture or the default picture.
account_id = '8730414'
# Recipient Information:
#signer_name = 'Zachary Baird'
#signer_email = 'zachbairddev@gmail.com'
# The document you wish to send. Path is relative to the root directory of this repo.
file_name_path = 'demo_documents/World_Wide_Corp_lorem.pdf'
base_path = 'https://demo.docusign.net/restapi'

# Constants
APP_PATH = os.path.dirname(os.path.abspath(__file__))


def send_document_for_signing(signer_name, signer_email):
    """
    Sends the document <file_name> to be signed by <signer_name> via <signer_email>
    """

    # Create the component objects for the envelope definition...
    with open(os.path.join(APP_PATH, file_name_path), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    document = Document(  # create the DocuSign document object
        document_base64=base64_file_content,
        name='Example document',  # can be different from actual file name
        file_extension='pdf',  # many different document types are accepted
        document_id=1  # a label used to reference the doc
    )

    # Create the signer recipient model
    signer = Signer(  # The signer
        email=signer_email, name=signer_name, recipient_id="1", routing_order="1")

    # Create a sign_here tab (field on the document)
    sign_here = SignHere(  # DocuSign SignHere field/tab
        document_id='1', page_number='1', recipient_id='1', tab_label='SignHereTab',
        x_position='195', y_position='147')

    # Add the tabs model (including the sign_here tab) to the signer
    # The Tabs object wants arrays of the different field/tab types
    signer.tabs = Tabs(sign_here_tabs=[sign_here])

    # Next, create the top level envelope definition and populate it.
    envelope_definition = EnvelopeDefinition(
        email_subject="Please sign this document sent from the Python SDK",
        # The order in the docs array determines the order in the envelope
        documents=[document],
        # The Recipients object wants arrays for each recipient type
        recipients=Recipients(signers=[signer]),
        status="sent"  # requests that the envelope be created and sent.
    )

    # Ready to go: send the envelope request
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", "Bearer " + access_token)

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(
        account_id, envelope_definition=envelope_definition)
    return results