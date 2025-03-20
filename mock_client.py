import random
from datetime import datetime, timedelta
import base64


class MockClient:
    #------------ 1 CustomerAuthenticationAPI--------------------------------------
    def customer_authentication(self, customerId, pin, mobileNumber, deviceId):
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
    def account_validation(self, accountNumber, accountType, mobileNumber, authToken, sessionId):
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
    def balance_inquiry(self, accountNumber, authToken, mobileNumber, sessionId):
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
    def beneficiary_validation(self, beneficiaryAccountNumber, beneficiaryBank, ifscCode, mobileNumber, authToken, sessionId):
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
    def fund_availability_check(self, accountNumber, amount, mobileNumber, authToken, sessionId):
        available_balance = 5240.75
        applicable_charges = 5.00

        amount = float(amount)  # Convert amount from string to float

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
    def transfer_authentication(self, accountNumber, transactionPassword, mobileNumber, authToken, sessionId):
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
    def initiate_transfer(self, sourceAccountNumber, beneficiaryAccountNumber, amount, mobileNumber, transferPurpose, remarks,
                          transactionId, authorizationCode, authToken, sessionId):
        # Ensure amount is a float
        amount = float(amount) if isinstance(amount, str) else amount
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
# --------------------- 8 GetUserBills -----------------------------------

    def get_user_bills(self, mobileNumber, authToken, sessionId):
        if mobileNumber == "+919876543210":
            return {
                "GetUserBillsResult": [
                    {
                        "BillerId": "BIL001",
                        "BillType": "Electricity",
                        "BillerName": "Metro Power Co.",
                        "ConsumerNumber": "EL123456789",
                        "CustomerName": "John Doe",
                        "BillNumber": "INV987654321",
                        "BillDate": "2025-03-01",
                        "DueDate": "2025-03-25",
                        "BillAmount": 128.45,
                        "BillPeriod": "Feb 2025",
                        "BillStatus": "Unpaid",
                        "LateCharges": 0.00,
                        "PaymentId": "PYM123456789"
                    },
                    {
                        "BillerId": "BIL002",
                        "BillType": "Water",
                        "BillerName": "City Water Supply",
                        "ConsumerNumber": "WT987654321",
                        "CustomerName": "John Doe",
                        "BillNumber": "WAT123456",
                        "BillDate": "2025-03-05",
                        "DueDate": "2025-03-30",
                        "BillAmount": 75.20,
                        "BillPeriod": "Feb 2025",
                        "BillStatus": "Unpaid",
                        "LateCharges": 0.00,
                        "PaymentId": "PYM222222222"
                    }
                ],
                "returnMessage": "Bills retrieved successfully"
            }
        else:
            return {
                "GetUserBillsResult": [],
                "returnMessage": "No bills found for this mobile number"
            }
# ----------------- 9 BillValidationAPI -----------------------------------
    def validate_bill(self, consumerNumber, mobileNumber, authToken, sessionId):
        bills = {
            "EL123456789": {
                "billerId": "BIL001",
                "billType": "Electricity",
                "billerName": "Metro Power Co.",
                "customerName": "John Doe",
                "billNumber": "INV987654321",
                "billDate": "2025-03-01",
                "dueDate": "2025-03-25",
                "billAmount": 128.45,
                "billPeriod": "Feb 2025",
                "billStatus": "Unpaid",
                "lateCharges": 0.00,
                "returnMessage": "Bill details retrieved successfully",
                "result": 1
            }
        }

        if sessionId != "SES123456789":
            return {"result": -3, "returnMessage": "Invalid session"}

        bill = bills.get(consumerNumber)
        if bill:
            return {"BillValidationResult": bill["result"], **bill}
        else:
            return {"BillValidationResult": -2, "returnMessage": "Bill not found or invalid consumer number"}

#------------------------- 10 ProcessBillPaymentApi ------------------------------
    def process_payment(self, accountNumber, consumerNumber, paymentId, authorizationCode, mobileNumber, authToken,
                        sessionId):
        # Mocked database of bills and payments
        payments = {
            "PYM123456789": {
                "paymentReferenceNumber": "PYREF123456789",
                "paymentStatus": "Completed",
                "paymentDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "paidAmount": 128.45,
                "billerName": "Metro Power Co.",
                "billPeriod": "Feb 2025",
                "remainingBalance": 5112.30,
                "receiptNumber": "REC123456789",
                "returnMessage": "Bill payment successful",
                "result": 1
            }
        }

        if sessionId != "SES123456789":
            return {"ProcessBillPaymentResult": -3, "returnMessage": "Invalid session",
                    "paymentReferenceNumber": "ERROR123456789", "paymentStatus": "Failed"}

        payment = payments.get(paymentId)
        if payment:
            return {"ProcessBillPaymentResult": payment["result"], **payment}
        else:
            return {"ProcessBillPaymentResult": -2, "returnMessage": "Payment failed due to technical issues",
                    "paymentReferenceNumber": "ERROR123456789", "paymentStatus": "Failed"}

# ------------- 11 PaymentAuthenticationCheckAPI ------------------------------
    def authenticate_payment(self, accountNumber, pin, mobileNumber, authToken, sessionId):
        # Hardcoded valid credentials
        valid_accounts = {
            "1098765432109": {"pin": "123456", "paymentId": "PYM123456789", "authorizationCode": "PAUTH98765"}
        }
        remaining_attempts = {"1098765432109": 3}  # Track attempts per account

        # Validate session
        if sessionId != "SES123456789":
            return {
                "PaymentAuthenticationCheckResult": -3,
                "returnMessage": "Invalid session",
                "remainingAttempts": remaining_attempts.get(accountNumber, 3)
            }

        # Check if account exists
        if accountNumber in valid_accounts:
            account = valid_accounts[accountNumber]

            # Validate PIN
            if account["pin"] == pin:
                valid_until = (datetime.utcnow() + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")

                return {
                    "PaymentAuthenticationCheckResult": 1,
                    "paymentId": account["paymentId"],
                    "authorizationCode": account["authorizationCode"],
                    "validUntil": valid_until,
                    "remainingAttempts": 3,
                    "returnMessage": "Payment authentication successful"
                }
            else:
                remaining_attempts[accountNumber] = max(remaining_attempts[accountNumber] - 1, 0)

                return {
                    "PaymentAuthenticationCheckResult": -2,
                    "returnMessage": "Invalid PIN",
                    "remainingAttempts": remaining_attempts[accountNumber]
                }

        return {
            "PaymentAuthenticationCheckResult": -1,
            "returnMessage": "Account not found",
            "remainingAttempts": 0
        }

# --------------- 12 ReceiptGenerationApi -----------------------
    def generate_receipt(self, paymentReferenceNumber, receiptNumber, mobileNumber, authToken, sessionId):
        # Hardcoded valid data
        valid_payments = {
            "PYREF123456789": {
                "receiptNumber": "REC123456789",
                "billerName": "Metro Power Co.",
                "consumerNumber": "EL123456789",
                "billNumber": "INV987654321",
                "paidAmount": 128.45,
                "paymentStatus": "Completed",
                "paymentDate": "2025-03-17T14:30:45Z"
            }
        }

        # Validate session
        if sessionId != "SES123456789":
            return {
                "ReceiptGenerationResult": -3,
                "returnMessage": "Invalid session"
            }

        # Check if payment reference exists
        if paymentReferenceNumber in valid_payments:
            payment_data = valid_payments[paymentReferenceNumber]

            # Validate receipt number
            if payment_data["receiptNumber"] == receiptNumber:
                receiptTimestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                fake_pdf_data = base64.b64encode(b"Fake PDF Receipt Data").decode()

                return {
                    "ReceiptGenerationResult": 1,
                    "receiptFormat": "PDF",
                    "receiptData": fake_pdf_data,
                    "receiptTimestamp": receiptTimestamp,
                    "billerName": payment_data["billerName"],
                    "consumerNumber": payment_data["consumerNumber"],
                    "billNumber": payment_data["billNumber"],
                    "paidAmount": payment_data["paidAmount"],
                    "paymentStatus": payment_data["paymentStatus"],
                    "paymentDate": payment_data["paymentDate"],
                    "returnMessage": "Receipt generated successfully"
                }

        return {
            "ReceiptGenerationResult": -2,
            "returnMessage": "Receipt generation failed. Invalid payment reference."
        }

# ---------------- 13 FetchMiniStatementApi ------------------
    def fetch_mini_statement(self, accountNumber, numberOfTransactions=10, fromDate=None, toDate=None, mobileNumber=None,
                             authToken=None, sessionId=None):
        # Hardcoded valid account data
        valid_accounts = {
            "1098765432109": {
                "accountName": "John Doe",
                "transactions": [
                    {"date": "2025-03-17T14:30:45Z", "type": "DEBIT", "description": "Bill Payment - Metro Power Co.",
                     "amount": 128.45, "reference": "PYREF123456789", "status": "Completed"},
                    {"date": "2025-03-15T10:45:22Z", "type": "CREDIT", "description": "Salary Credit",
                     "amount": 5000.00, "reference": "SALARY032025", "status": "Completed"},
                    {"date": "2025-03-10T08:12:30Z", "type": "DEBIT", "description": "Grocery Shopping",
                     "amount": 322.30, "reference": "GROC123456789", "status": "Completed"}
                ],
                "currentBalance": 5112.30,
                "availableBalance": 5112.30,
                "openingBalance": 563.05,
                "closingBalance": 5112.30,
                "totalDebits": 450.75,
                "totalCredits": 5000.00
            }
        }

        # Validate session
        if sessionId != "SES123456789":
            return {
                "FetchMiniStatementResult": -3,
                "returnMessage": "Invalid session"
            }

        # Validate account number
        if accountNumber not in valid_accounts:
            return {
                "FetchMiniStatementResult": -2,
                "returnMessage": "Unauthorized access to account information"
            }

        account_data = valid_accounts[accountNumber]
        transactions = account_data["transactions"]

        # Apply date filtering
        if fromDate and toDate:
            transactions = [
                txn for txn in transactions if fromDate <= txn["date"][:10] <= toDate
            ]

        # Ensure numberOfTransactions is an integer
        if numberOfTransactions is None:
            numberOfTransactions = 10  # Default value
        elif isinstance(numberOfTransactions, str) and numberOfTransactions.isdigit():
            numberOfTransactions = int(numberOfTransactions)

        # Limit number of transactions safely
        transactions = transactions[:numberOfTransactions]

        return {
            "FetchMiniStatementResult": 1,
            "transactionDates": [txn["date"] for txn in transactions],
            "transactionTypes": [txn["type"] for txn in transactions],
            "descriptions": [txn["description"] for txn in transactions],
            "amounts": [txn["amount"] for txn in transactions],
            "transactionReferences": [txn["reference"] for txn in transactions],
            "statuses": [txn["status"] for txn in transactions],
            "currentBalance": account_data["currentBalance"],
            "availableBalance": account_data["availableBalance"],
            "accountName": account_data["accountName"],
            "totalDebits": account_data["totalDebits"],
            "totalCredits": account_data["totalCredits"],
            "openingBalance": account_data["openingBalance"],
            "closingBalance": account_data["closingBalance"],
            "returnMessage": "Mini statement fetched successfully"
        }

# ---------- 14 ProcessChequeBookRequest Api --------------------------------
    def process_cheque_book_request(self, accountNumber, numberOfLeaves, deliveryOption, branchCode=None,
                                    reasonForRequest=None, additionalRemarks=None, mobileNumber=None, authToken=None,
                                    sessionId=None):
        # Hardcoded valid accounts
        valid_accounts = {"1098765432109": {"eligible": True}}

        # Validate session
        if sessionId != "SES123456789":
            return {
                "ProcessChequeBookRequestResult": -3,
                "returnMessage": "Invalid session"
            }

        # Validate account number
        if accountNumber not in valid_accounts:
            return {
                "ProcessChequeBookRequestResult": -2,
                "returnMessage": "Technical Error"
            }

        # Check account eligibility
        if not valid_accounts[accountNumber]["eligible"]:
            return {
                "ProcessChequeBookRequestResult": -4,
                "returnMessage": "Account not eligible for cheque book"
            }

        # Validate delivery option and branch code
        if deliveryOption == "Branch Pickup" and not branchCode:
            return {
                "ProcessChequeBookRequestResult": -1,
                "returnMessage": "Branch code is required for Branch Pickup"
            }

        # Generate response details
        requestReferenceNumber = f"CHQ{random.randint(100000000, 999999999)}"
        requestStatus = "Confirmed"
        requestDate = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        estimatedDeliveryDate = (datetime.utcnow() + timedelta(days=10)).strftime("%Y-%m-%d")
        deliveryMethod = deliveryOption
        processingCharges = 25.00

        return {
            "ProcessChequeBookRequestResult": 1,
            "requestReferenceNumber": requestReferenceNumber,
            "requestStatus": requestStatus,
            "requestDate": requestDate,
            "estimatedDeliveryDate": estimatedDeliveryDate,
            "deliveryMethod": deliveryMethod,
            "processingCharges": processingCharges,
            "returnMessage": "Cheque book request processed successfully"
        }