import sys
import json
from client import FormatConverter

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-alpaca-sharegpt-format-converter-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "convert_alpaca_to_sharegpt",
                        "description": "Converts Alpaca instruction JSON record to ShareGPT multi-turn conversation format",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "record": {"type": "object"}
                            },
                            "required": ["record"]
                        }
                    },
                    {
                        "name": "convert_sharegpt_to_alpaca",
                        "description": "Converts ShareGPT conversation record to Alpaca instruction format",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "record": {"type": "object"}
                            },
                            "required": ["record"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "convert_alpaca_to_sharegpt":
            res = FormatConverter.alpaca_to_sharegpt(args.get("record", {}))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif name == "convert_sharegpt_to_alpaca":
            res = FormatConverter.sharegpt_to_alpaca(args.get("record", {}))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def run():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run()
