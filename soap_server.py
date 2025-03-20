from flask import Flask, request, Response
from zeep import Client
from zeep.plugins import HistoryPlugin
from lxml import etree
import io
import re

# Import your existing MockClient
from mock_client import MockClient  # Assuming your class is in mock_client.py

class ZeepMockClient:
    def __init__(self):
        self.mock_client = MockClient()
    
    def _create_soap_response(self, service_name, json_response):
        """Create a SOAP response using lxml"""
        # Create XML for response
        root = etree.Element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope')
        body = etree.SubElement(root, '{http://schemas.xmlsoap.org/soap/envelope/}Body')
        
        # Create response element with appropriate namespace
        namespace = "http://tempuri.org/"
        response = etree.SubElement(body, f'{{{namespace}}}{service_name}Response')
        result = etree.SubElement(response, f'{service_name}Result')
        
        # Add response fields
        for key, value in json_response.items():
            elem = etree.SubElement(result, key)
            if value is not None:
                if isinstance(value, bool):
                    elem.text = str(value).lower()
                else:
                    elem.text = str(value)
            else:
                elem.text = ""
                
        # Convert to string
        return etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')
    
    def _create_soap_fault(self, fault_code, fault_string):
        """Create a SOAP fault response"""
        root = etree.Element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope')
        body = etree.SubElement(root, '{http://schemas.xmlsoap.org/soap/envelope/}Body')
        fault = etree.SubElement(body, '{http://schemas.xmlsoap.org/soap/envelope/}Fault')
        
        code = etree.SubElement(fault, 'faultcode')
        code.text = fault_code
        
        string = etree.SubElement(fault, 'faultstring')
        string.text = fault_string
        
        return etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')
    
    # API method implementations that wrap the MockClient methods
    def customer_authentication(self, customerId, pin, mobileNumber, deviceId):
        json_response = self.mock_client.customer_authentication(customerId, pin, mobileNumber, deviceId)
        return self._create_soap_response('CustomerAuthentication', json_response)
    
    def account_validation(self, accountNumber, accountType, mobileNumber, authToken, sessionId):
        json_response = self.mock_client.account_validation(accountNumber, accountType, mobileNumber, authToken, sessionId)
        return self._create_soap_response('AccountValidation', json_response)
    
    def balance_inquiry(self, accountNumber, authToken, mobileNumber, sessionId):
        json_response = self.mock_client.balance_inquiry(accountNumber, authToken, mobileNumber, sessionId)
        return self._create_soap_response('BalanceInquiry', json_response)
    
    def beneficiary_validation(self, beneficiaryAccountNumber, beneficiaryBank, ifscCode, mobileNumber, authToken, sessionId):
        json_response = self.mock_client.beneficiary_validation(beneficiaryAccountNumber, beneficiaryBank, ifscCode, mobileNumber, authToken, sessionId)
        return self._create_soap_response('BeneficiaryValidation', json_response)
    
    def fund_availability_check(self, accountNumber, amount, mobileNumber, authToken, sessionId):
        json_response = self.mock_client.fund_availability_check(accountNumber, amount, mobileNumber, authToken, sessionId)
        return self._create_soap_response('FundAvailabilityCheck', json_response)
    
    def transfer_authentication(self, accountNumber, transactionPassword, mobileNumber, authToken, sessionId):
        json_response = self.mock_client.transfer_authentication(accountNumber,  transactionPassword,mobileNumber, authToken, sessionId)
        return self._create_soap_response('TransferAuthentication', json_response)
    
    def initiate_transfer(self, sourceAccountNumber, beneficiaryAccountNumber, amount, mobileNumber, transferPurpose, remarks,
                         transactionId, authorizationCode, authToken, sessionId):
        json_response = self.mock_client.initiate_transfer(sourceAccountNumber, beneficiaryAccountNumber, mobileNumber, amount,
                                                         transferPurpose, remarks, transactionId, authorizationCode, 
                                                         authToken, sessionId)
        return self._create_soap_response('InitiateTransfer', json_response)
# --------------- After 7   --------------------------------------------------------

    def get_user_bills(self, mobileNumber, authToken, sessionId):
        json_response = self.mock_client.get_user_bills(mobileNumber, authToken, sessionId)
        return self._create_soap_response('GetUserBills', json_response)

    def bill_validation(self, consumerNumber, mobileNumber, authToken, sessionId):
        json_response = self.mock_client.validate_bill(consumerNumber, mobileNumber, authToken, sessionId)
        return self._create_soap_response('BillValidation', json_response)

    def process_bill_payment(self, accountNumber, consumerNumber, paymentId, authorizationCode, mobileNumber, authToken,
                        sessionId):
        json_response = self.mock_client.process_payment(accountNumber, consumerNumber, paymentId, authorizationCode,
                                                         mobileNumber, authToken, sessionId)
        return self._create_soap_response('ProcessBillPayment', json_response)

    def payment_authentication_check(self, accountNumber, pin, mobileNumber, authToken, sessionId):
        json_response = self.mock_client.authenticate_payment(accountNumber, pin, mobileNumber, authToken, sessionId)
        return self._create_soap_response('PaymentAuthenticationCheck', json_response)

    def generate_receipt(self, paymentReferenceNumber, receiptNumber, mobileNumber, authToken, sessionId):
        json_response = self.mock_client.generate_receipt(paymentReferenceNumber, receiptNumber, mobileNumber,
                                                          authToken, sessionId)
        return self._create_soap_response('ReceiptGeneration', json_response)

    def fetch_mini_statement(self, accountNumber, numberOfTransactions=10, fromDate=None, toDate=None,
                             mobileNumber=None, authToken=None, sessionId=None):
        json_response = self.mock_client.fetch_mini_statement(accountNumber, numberOfTransactions, fromDate, toDate,
                                                              mobileNumber, authToken, sessionId)
        return self._create_soap_response('FetchMiniStatement', json_response)

    def process_cheque_book_request(self, accountNumber, numberOfLeaves, deliveryOption, branchCode=None,
                                    reasonForRequest=None, additionalRemarks=None, mobileNumber=None, authToken=None,
                                    sessionId=None):
        json_response = self.mock_client.process_cheque_book_request(accountNumber, numberOfLeaves, deliveryOption,
                                                                     branchCode, reasonForRequest, additionalRemarks,
                                                                     mobileNumber, authToken, sessionId)
        return self._create_soap_response('ProcessChequeBookRequest', json_response)
    


# Create Flask app and zeep mock client
app = Flask(__name__)
zeep_mock = ZeepMockClient()

# Helper function to extract parameters from SOAP request
def extract_soap_params(xml_string, operation_name):
    """Extract parameters from SOAP request XML"""
    try:
        # Parse XML
        root = etree.fromstring(xml_string)
        
        # Define namespaces (these would be from your actual WSDL)
        nsmap = {
            'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsd': 'http://www.w3.org/2001/XMLSchema',
            # Add your service namespace here, for simplicity we'll use a default one
            'ser': 'http://tempuri.org/'
        }
        
        # Find operation element in body
        operation_path = f".//ser:{operation_name}"
        operation_elem = root.xpath(operation_path, namespaces=nsmap)
        
        if not operation_elem:
            # Try without namespace if not found
            operation_elem = root.xpath(f".//*[local-name()='{operation_name}']")
            
        if not operation_elem:
            return {}
            
        # Extract parameters
        params = {}
        for child in operation_elem[0]:
            tag = etree.QName(child).localname
            params[tag] = child.text
            
        return params
    except Exception as e:
        print(f"Error parsing SOAP request: {e}")
        return {}

# SOAP service endpoint
@app.route('/soap/<service_name>', methods=['POST'])
def soap_service(service_name):
    # Get the raw SOAP request
    soap_request = request.data.decode('utf-8')
    
    try:
        # Map service names to methods
        service_method_map = {
            'CustomerAuthentication': zeep_mock.customer_authentication,
            'AccountValidation': zeep_mock.account_validation,
            'BalanceInquiry': zeep_mock.balance_inquiry,
            'BeneficiaryValidation': zeep_mock.beneficiary_validation,
            'FundAvailabilityCheck': zeep_mock.fund_availability_check,
            'TransferAuthentication': zeep_mock.transfer_authentication,
            'InitiateTransfer': zeep_mock.initiate_transfer,
            'GetUserBills':zeep_mock.get_user_bills,
            'BillValidation':zeep_mock.bill_validation,
            'ProcessBillPayment':zeep_mock.process_bill_payment,
            'PaymentAuthenticationCheck':zeep_mock.payment_authentication_check,
            'ReceiptGeneration':zeep_mock.generate_receipt,
            'FetchMiniStatement':zeep_mock.fetch_mini_statement,
            'ProcessChequeBookRequest':zeep_mock.process_cheque_book_request
        }
        
        # Check if service exists
        if service_name not in service_method_map:
            return Response(
                zeep_mock._create_soap_fault('Client', f'Unknown service: {service_name}'),
                mimetype='text/xml'
            )
        
        # Extract parameters from the SOAP request
        params = extract_soap_params(soap_request, service_name)
        
        # Call the appropriate method with the extracted parameters
        service_method = service_method_map[service_name]
        soap_response = service_method(**params)
        
        # Return the SOAP response
        return Response(soap_response, mimetype='text/xml')
    except Exception as e:
        # Return SOAP fault in case of error
        return Response(
            zeep_mock._create_soap_fault('Server', str(e)),
            mimetype='text/xml'
        )

if __name__ == '__main__':
    # For Docker, we need to listen on 0.0.0.0 instead of localhost
    app.run(debug=True, host='0.0.0.0', port=8000)