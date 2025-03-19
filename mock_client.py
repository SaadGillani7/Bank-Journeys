import random
from datetime import datetime


class MockClient:
    #------------ 1 CustomerAuthenticationAPI--------------------------------------
    def customer_authentication(self, customerId, pin, deviceId):
        if customerId == "CUS123456" and pin == "123456":
            return {
                "CustomerAuthenticationResult": "1",
                "returnMessage": "Authentication successful",
                "customerName": "John Doe",
                "authToken": "ae72fe105744b7fd8139bda4098a404455e0f891c2c425a709116",
                "sessionId": "SES123456789",
                "sessionTimeout": 300,
                "lastLogin": datetime.utcnow().isoformat(),
                "isBlocked": False
            }
        else:
            return {
                "CustomerAuthenticationResult": "-2",
                "returnMessage": "Invalid customer credentials",
                "customerName": "",
                "authToken": "",
                "sessionId": "",
                "sessionTimeout": 0,
                "lastLogin": "",
                "isBlocked": False
            }
            
    #--------------- 2 AccountValidationAPI ---------------------------------------
    def account_validation(self, accountNumber, accountType, authToken, sessionId):
        if accountNumber == "1098765432109" and accountType == "Savings":
            return {
                "AccountValidationResult": "1",
                "returnMessage": "Account validation successful",
                "accountStatus": "Active",
                "branchCode": "BR001",
                "currencyCode": "USD",
                "maskedAccountNumber": "XXXX5432109"
            }
        else:
            return {
                "AccountValidationResult": "-2",
                "returnMessage": "Account not found or doesn't belong to the customer",
                "accountStatus": "",
                "branchCode": "",
                "currencyCode": "",
                "maskedAccountNumber": ""
            }
            
    # --------------- 3 BalanceInquiryAPI ------------------------------------
    def balance_inquiry(self, accountNumber, authToken, sessionId):
        if accountNumber == "1098765432109":
            return {
                "BalanceInquiryResult": "1",
                "returnMessage": "Balance inquiry successful",
                "availableBalance": 5240.75,
                "ledgerBalance": 5240.75,
                "holdAmount": 0.00,
                "overdraftLimit": 1000.00,
                "currencyCode": "USD",
                "lastTransactionDate": datetime.utcnow().isoformat()
            }
        else:
            return {
                "BalanceInquiryResult": "-2",
                "returnMessage": "Unauthorized access to account information",
                "availableBalance": 0,
                "ledgerBalance": 0,
                "holdAmount": 0,
                "overdraftLimit": 0,
                "currencyCode": "",
                "lastTransactionDate": ""
            }

    #------------------- 4 BeneficiaryValidation ------------------------
    def beneficiary_validation(self, beneficiaryAccountNumber, beneficiaryBank, ifscCode, authToken, sessionId):
        if beneficiaryAccountNumber == "2098765432109" and beneficiaryBank == "HDFC Bank":
            return {
                "BeneficiaryValidationResult": "1",
                "returnMessage": "Beneficiary validation successful",
                "beneficiaryName": "Jane Smith",
                "maskedAccountNumber": "XXXX5432109",
                "bankName": "HDFC Bank",
                "branchName": "Downtown Branch"
            }
        else:
            return {
                "BeneficiaryValidationResult": "-2",
                "returnMessage": "Invalid beneficiary details",
                "beneficiaryName": "",
                "maskedAccountNumber": "",
                "bankName": "",
                "branchName": ""
            }
            
    # ---------------- 5 FundAvailabilityCheckAPI ------------------------
    def fund_availability_check(self, accountNumber, amount, authToken, sessionId):
        available_balance = 5240.75
        applicable_charges = 5.00
        total_debitable = amount + applicable_charges
        is_sufficient = total_debitable <= available_balance
        shortfall = 0.00 if is_sufficient else total_debitable - available_balance

        if is_sufficient:
            return {
                "FundAvailabilityCheckResult": "1",
                "returnMessage": "Sufficient funds available",
                "availableBalance": available_balance,
                "isSufficient": is_sufficient,
                "applicableCharges": applicable_charges,
                "totalDebitable": total_debitable,
                "shortfall": shortfall
            }
        else:
            return {
                "FundAvailabilityCheckResult": "2",
                "returnMessage": "Insufficient funds",
                "availableBalance": available_balance,
                "isSufficient": is_sufficient,
                "applicableCharges": 0.00,
                "totalDebitable": 0.00,
                "shortfall": shortfall
            }

    # -------------------- 6 TransferAuthenticationAPI -----------------------------
    def transfer_authentication(self, accountNumber, transactionPassword, authToken, sessionId):
        if transactionPassword == "Tr@n$123":
            return {
                "TransferAuthenticationResult": "1",
                "returnMessage": "Transfer authentication successful",
                "transactionId": "TXN123456789",
                "authorizationCode": "AUTH98765",
                "validUntil": datetime.utcnow().isoformat(),
                "remainingAttempts": 3
            }
        else:
            return {
                "TransferAuthenticationResult": "-2",
                "returnMessage": "Invalid transaction password",
                "transactionId": "",
                "authorizationCode": "",
                "validUntil": "",
                "remainingAttempts": 2
            }

    # ---------------------- 7 InitiateTransferAPI -----------------------
    def initiate_transfer(self, sourceAccountNumber, beneficiaryAccountNumber, amount, transferPurpose, remarks,
                          transactionId, authorizationCode, authToken, sessionId):
        if sourceAccountNumber == "1098765432109" and beneficiaryAccountNumber == "2098765432109":
            return {
                "InitiateTransferResult": "1",
                "returnMessage": "Transfer successful",
                "transactionReferenceNumber": "REF123456789",
                "transactionStatus": "Completed",
                "transactionDate": datetime.utcnow().isoformat(),
                "transferredAmount": amount,
                "charges": 5.00,
                "totalDebited": amount + 5.00,
                "beneficiaryName": "Jane Smith",
                "maskedBeneficiaryAccountNumber": "XXXX5432109",
                "beneficiaryBank": "HDFC Bank",
                "remainingBalance": 4235.75
            }
        else:
            return {
                "InitiateTransferResult": "-2",
                "returnMessage": "Transfer failed due to technical issues",
                "transactionReferenceNumber": "ERROR123456789",
                "transactionStatus": "Failed",
                "transactionDate": datetime.utcnow().isoformat(),
                "transferredAmount": 0,
                "charges": 0,
                "totalDebited": 0,
                "beneficiaryName": "",
                "maskedBeneficiaryAccountNumber": "",
                "beneficiaryBank": "",
                "remainingBalance": 5240.75
            }

    # -------------------- 8 BillValidationAPI ----------------------------------
    def bill_validation(self, billType, billerName, consumerNumber, authToken, sessionId):
        if consumerNumber == "EL123456789":
            return {
                "BillValidationResult": "1",
                "returnMessage": "Bill details retrieved successfully",
                "billerId": "BIL001",
                "customerName": "John Doe",
                "billNumber": "INV987654321",
                "billDate": "2025-03-01",
                "dueDate": "2025-03-25",
                "billAmount": 128.45,
                "billPeriod": "Feb 2025",
                "billStatus": "Unpaid",
                "lateCharges": 0.00
            }
        else:
            return {
                "BillValidationResult": "-2",
                "returnMessage": "Bill not found or invalid consumer number",
                "billerId": "",
                "customerName": "",
                "billNumber": "",
                "billDate": "",
                "dueDate": "",
                "billAmount": 0,
                "billPeriod": "",
                "billStatus": "",
                "lateCharges": 0
            }

    # --------------------- 9 PaymentAuthenticationCheckAPI ----------------------
    def payment_authentication_check(self, accountNumber, pin, authToken, sessionId):
        if accountNumber == "1098765432109" and pin == "123456":
            return {
                "PaymentAuthenticationCheckResult": "1",
                "returnMessage": "Payment authentication successful",
                "paymentId": "PYM123456789",
                "authorizationCode": "PAUTH98765",
                "validUntil": "2025-03-17T15:45:30Z",
                "remainingAttempts": 3
            }
        else:
            return {
                "PaymentAuthenticationCheckResult": "-2",
                "returnMessage": "Invalid PIN",
                "paymentId": "",
                "authorizationCode": "",
                "validUntil": "",
                "remainingAttempts": 2
            }

    #---------- 10 ProcessBillPayment --------------------------------------
    def process_bill_payment(self, accountNumber, billerId, consumerNumber, billNumber, amount, paymentId,
                             authorizationCode, authToken, sessionId):
        # Simulating session validation
        if sessionId == "666":
            return {
                "ProcessBillPaymentResult": "-3",
                "returnMessage": "Invalid Session",
                "paymentReferenceNumber": "ERROR123456789",
                "paymentStatus": "Failed",
                "paymentDate": datetime.utcnow().isoformat(),
                "paidAmount": 0,
                "billerName": "",
                "billPeriod": "",
                "remainingBalance": 0,
                "receiptNumber": ""
            }
        else:
            # Generate a receipt number to be used in receipt generation
            receipt_number = f"REC{random.randint(100000000, 999999999)}"
            
            # In a real implementation, you might store this for later retrieval
            self.last_receipt_number = receipt_number
            
            return {
                "ProcessBillPaymentResult": "1",
                "returnMessage": "Bill payment successful",
                "paymentReferenceNumber": f"PYREF{random.randint(100000000, 999999999)}",
                "paymentStatus": "Completed",
                "paymentDate": datetime.utcnow().isoformat(),
                "paidAmount": amount,
                "billerName": "Metro Power Co.",
                "billPeriod": "Feb 2025",
                "remainingBalance": 5112.30,
                "receiptNumber": receipt_number
            }