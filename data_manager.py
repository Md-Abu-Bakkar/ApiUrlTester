import json
import os
from datetime import datetime

class DataManager:
    def __init__(self, base_path="."):
        self.base_path = base_path
        self.ensure_directories()
        
    def ensure_directories(self):
        """Ensure all necessary directories exist"""
        os.makedirs(self.base_path, exist_ok=True)
        
    def save_response(self, response_data):
        """Save API response to multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save to data.json (append to array)
        self._save_to_json('data.json', response_data)
        
        # Save to data.txt (human readable)
        self._save_to_txt('data.txt', response_data)
        
        # Check for earnings and save accordingly
        self._check_earnings(response_data)
        
        # Log to system log
        self._log_system(response_data)
        
    def _save_to_json(self, filename, data):
        filepath = os.path.join(self.base_path, filename)
        
        try:
            # If file exists, load and append
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    try:
                        existing_data = json.load(f)
                        if isinstance(existing_data, list):
                            existing_data.append(data)
                        else:
                            existing_data = [existing_data, data]
                    except json.JSONDecodeError:
                        existing_data = [data]
            else:
                existing_data = [data]
                
            # Save back to file
            with open(filepath, 'w') as f:
                json.dump(existing_data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            
    def _save_to_txt(self, filename, data):
        filepath = os.path.join(self.base_path, filename)
        
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Timestamp: {data.get('timestamp', 'N/A')}\n")
                f.write(f"URL: {data.get('url', 'N/A')}\n")
                f.write(f"Method: {data.get('method', 'N/A')}\n")
                f.write(f"Status Code: {data.get('status_code', 'N/A')}\n")
                f.write(f"Response Time: {data.get('response_time', 0):.2f}s\n")
                f.write(f"Success: {data.get('success', False)}\n")
                
                response = data.get('response', {})
                if isinstance(response, dict):
                    f.write("Response:\n")
                    f.write(json.dumps(response, indent=2))
                else:
                    f.write(f"Response: {response}")
                    
                f.write(f"\n{'='*50}\n")
                
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            
    def _check_earnings(self, data):
        """Check if response contains earnings data and save accordingly"""
        response = data.get('response', {})
        
        # Look for common earnings/coins/points fields
        earnings_keys = ['earnings', 'coins', 'points', 'balance', 'money', 'reward']
        
        for key in earnings_keys:
            if isinstance(response, dict) and key in response:
                earnings_data = {
                    'timestamp': data.get('timestamp'),
                    'type': key,
                    'amount': response[key],
                    'url': data.get('url'),
                    'method': data.get('method')
                }
                
                self._save_to_json('earnings.json', earnings_data)
                self._log_earnings(earnings_data)
                break
                
    def _log_earnings(self, earnings_data):
        filepath = os.path.join(self.base_path, 'earnings.log')
        
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(f"{earnings_data['timestamp']} | {earnings_data['type']}: {earnings_data['amount']} | {earnings_data['url']}\n")
        except Exception as e:
            print(f"Error logging earnings: {e}")
            
    def _log_system(self, data):
        filepath = os.path.join(self.base_path, 'system.log')
        
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                status = "SUCCESS" if data.get('success') else "FAILED"
                f.write(f"{data.get('timestamp')} | {status} | {data.get('method')} {data.get('url')} | Code: {data.get('status_code')} | Time: {data.get('response_time', 0):.2f}s\n")
        except Exception as e:
            print(f"Error logging to system: {e}")
            
    def export_data(self, format_type='json'):
        """Export all data in specified format"""
        if format_type == 'json':
            return self._export_json()
        elif format_type == 'csv':
            return self._export_csv()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
            
    def _export_json(self):
        """Export all data as JSON"""
        export_data = {}
        
        for filename in ['data.json', 'earnings.json']:
            filepath = os.path.join(self.base_path, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    export_data[filename.replace('.json', '')] = json.load(f)
                    
        return export_data
        
    def _export_csv(self):
        """Export data as CSV (simplified)"""
        # Implementation for CSV export
        pass