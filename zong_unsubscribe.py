"""
Zong VAS Unsubscribe Tool
Helps unsubscribe from unnecessary Value Added Services (VAS) offers on Zong sim
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

class ZongVASUnsubscriber:
    """Handle Zong VAS unsubscription"""
    
    def __init__(self, phone_number: str, api_key: Optional[str] = None):
        """
        Initialize Zong VAS Unsubscriber
        
        Args:
            phone_number: Zong phone number
            api_key: Optional API key for Zong services
        """
        self.phone_number = phone_number
        self.api_key = api_key
        self.base_url = "https://api.zong.com.pk"  # Base URL for Zong API
        self.headers = self._setup_headers()
        self.vas_codes = self._get_vas_codes()
    
    def _setup_headers(self) -> Dict:
        """Setup API headers"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Zong-VAS-Unsubscriber/1.0'
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers
    
    def _get_vas_codes(self) -> Dict[str, str]:
        """Get common Zong VAS service codes"""
        return {
            'news': '*900#',
            'sports': '*901#',
            'weather': '*902#',
            'jokes': '*903#',
            'horoscope': '*904#',
            'cricket': '*905#',
            'entertainment': '*906#',
            'music': '*907#',
            'movies': '*908#',
            'games': '*909#',
            'dating': '*910#',
            'fortune_telling': '*911#',
            'astrology': '*912#',
            'alerts': '*913#',
            'general_unsub': '*777#',  # General unsubscribe code
        }
    
    def unsubscribe_ussd(self, service_code: str) -> Dict:
        """
        Unsubscribe using USSD code
        
        Args:
            service_code: USSD code for the service
            
        Returns:
            Dictionary with unsubscription status
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'phone_number': self.phone_number,
            'service_code': service_code,
            'method': 'USSD',
            'status': 'pending',
            'message': f'Send {service_code} from your Zong number to unsubscribe'
        }
        return result
    
    def unsubscribe_sms(self, service_name: str) -> Dict:
        """
        Unsubscribe using SMS command
        
        Args:
            service_name: Name of the service to unsubscribe from
            
        Returns:
            Dictionary with unsubscription details
        """
        sms_commands = {
            'news': 'STOP NEWS to 5050',
            'sports': 'STOP SPORTS to 5050',
            'weather': 'STOP WEATHER to 5050',
            'jokes': 'STOP JOKES to 5050',
            'all_vas': 'STOP ALL to 5050',
        }
        
        command = sms_commands.get(service_name, 'STOP ALL to 5050')
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'phone_number': self.phone_number,
            'service': service_name,
            'method': 'SMS',
            'command': command,
            'status': 'pending',
            'message': f'Send SMS: {command}'
        }
        return result
    
    def unsubscribe_api(self, service_code: str) -> Dict:
        """
        Unsubscribe using Zong API
        
        Args:
            service_code: Service code to unsubscribe from
            
        Returns:
            API response
        """
        try:
            payload = {
                'msisdn': self.phone_number,
                'service_code': service_code,
                'action': 'unsubscribe'
            }
            
            # Note: This is a template. Adjust endpoint based on actual Zong API
            response = requests.post(
                f'{self.base_url}/vas/unsubscribe',
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            return {
                'timestamp': datetime.now().isoformat(),
                'phone_number': self.phone_number,
                'service_code': service_code,
                'method': 'API',
                'status': 'success' if response.status_code == 200 else 'failed',
                'status_code': response.status_code,
                'response': response.json() if response.status_code == 200 else response.text
            }
        
        except requests.exceptions.RequestException as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    def get_active_vas(self) -> Dict:
        """
        Get list of active VAS subscriptions
        
        Returns:
            List of active services
        """
        try:
            payload = {'msisdn': self.phone_number}
            
            response = requests.post(
                f'{self.base_url}/vas/active',
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'success' if response.status_code == 200 else 'failed',
                'active_services': response.json() if response.status_code == 200 else []
            }
        
        except requests.exceptions.RequestException as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    def unsubscribe_all(self) -> Dict:
        """
        Unsubscribe from all VAS services at once
        
        Returns:
            Unsubscription result
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'phone_number': self.phone_number,
            'method': 'Multiple Methods',
            'options': [
                {
                    'method': 'USSD',
                    'command': '*777#',
                    'description': 'Dial *777# to unsubscribe from all VAS'
                },
                {
                    'method': 'SMS',
                    'command': 'STOP ALL to 5050',
                    'description': 'Send SMS "STOP ALL" to 5050'
                },
                {
                    'method': 'Call',
                    'command': '111',
                    'description': 'Call customer service at 111'
                }
            ]
        }
        return result
    
    def print_instructions(self):
        """Print user-friendly instructions"""
        print("\n" + "="*60)
        print("ZONG VAS UNSUBSCRIPTION INSTRUCTIONS")
        print("="*60)
        print(f"\nPhone Number: {self.phone_number}\n")
        
        print("METHOD 1: USSD CODE (Fastest)")
        print("-" * 40)
        print("Dial: *777# (unsubscribe from all)")
        print("Or dial specific service codes:")
        for service, code in self.vas_codes.items():
            print(f"  {service.replace('_', ' ').title()}: {code}")
        
        print("\n\nMETHOD 2: SMS")
        print("-" * 40)
        print("Send: STOP ALL to 5050")
        print("Or send specific commands:")
        print("  STOP NEWS to 5050")
        print("  STOP SPORTS to 5050")
        print("  STOP WEATHER to 5050")
        
        print("\n\nMETHOD 3: CUSTOMER SERVICE")
        print("-" * 40)
        print("Call: 111 (from your Zong number)")
        print("Or call: +92-300-111-0111 (from any number)")
        
        print("\n\nMETHOD 4: ZONG APP/WEB PORTAL")
        print("-" * 40)
        print("Visit: https://www.zong.com.pk")
        print("Or download Zong Mobile App")
        
        print("\n" + "="*60 + "\n")


def main():
    """Main function"""
    
    # Example usage
    phone_number = input("Enter your Zong phone number: ").strip()
    
    unsubscriber = ZongVASUnsubscriber(phone_number)
    
    while True:
        print("\n" + "="*60)
        print("ZONG VAS UNSUBSCRIBER")
        print("="*60)
        print("\n1. View unsubscription methods")
        print("2. Get USSD code for specific service")
        print("3. Get SMS command for service")
        print("4. Unsubscribe from all services")
        print("5. View common VAS codes")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            unsubscriber.print_instructions()
        
        elif choice == '2':
            print("\nAvailable services:")
            for i, service in enumerate(unsubscriber.vas_codes.keys(), 1):
                print(f"{i}. {service.replace('_', ' ').title()}")
            
            service_choice = input("\nEnter service number or name: ").strip().lower()
            code = unsubscriber.vas_codes.get(service_choice)
            if code:
                result = unsubscriber.unsubscribe_ussd(code)
                print(f"\n{result['message']}")
        
        elif choice == '3':
            service = input("Enter service name (or 'all' for all_vas): ").strip().lower()
            result = unsubscriber.unsubscribe_sms(service)
            print(f"\nSend: {result['command']}")
        
        elif choice == '4':
            result = unsubscriber.unsubscribe_all()
            print(f"\nQuick options:")
            for option in result['options']:
                print(f"\n{option['method']}: {option['command']}")
                print(f"  ({option['description']})")
        
        elif choice == '5':
            print("\nCommon Zong VAS Codes:")
            for service, code in unsubscriber.vas_codes.items():
                print(f"  {service.replace('_', ' ').title()}: {code}")
        
        elif choice == '6':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
