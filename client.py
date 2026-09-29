"""Alpaca and ShareGPT Dataset Format Converter.
100% Python Standard Library.
"""

import json

class FormatConverter:
    """Converts and validates dataset formats between Alpaca and ShareGPT schemas."""
    @staticmethod
    def alpaca_to_sharegpt(alpaca_record: dict) -> dict:
        instruction = alpaca_record.get("instruction", "")
        input_text = alpaca_record.get("input", "")
        output_text = alpaca_record.get("output", "")

        human_prompt = f"{instruction}\n\nInput: {input_text}".strip() if input_text else instruction
        conversations = [
            {"from": "human", "value": human_prompt},
            {"from": "gpt", "value": output_text}
        ]
        return {
            "id": alpaca_record.get("id", "sample_0"),
            "conversations": conversations
        }

    @staticmethod
    def sharegpt_to_alpaca(sharegpt_record: dict) -> dict:
        convs = sharegpt_record.get("conversations", [])
        if len(convs) < 2:
            return {"instruction": "", "input": "", "output": ""}
        
        human_msg = convs[0].get("value", "")
        gpt_msg = convs[1].get("value", "")

        if "\n\nInput: " in human_msg:
            parts = human_msg.split("\n\nInput: ", 1)
            instruction = parts[0]
            inp = parts[1]
        else:
            instruction = human_msg
            inp = ""

        return {
            "id": sharegpt_record.get("id", "sample_0"),
            "instruction": instruction,
            "input": inp,
            "output": gpt_msg
        }

    @staticmethod
    def validate_schema(record: dict, format_type: str = "alpaca") -> dict:
        errors = []
        if format_type == "alpaca":
            for field in ["instruction", "output"]:
                if field not in record:
                    errors.append(f"Missing required Alpaca field '{field}'")
        elif format_type == "sharegpt":
            if "conversations" not in record or not isinstance(record["conversations"], list):
                errors.append("Missing required ShareGPT field 'conversations' list")
            else:
                for idx, msg in enumerate(record["conversations"]):
                    if "from" not in msg or "value" not in msg:
                        errors.append(f"Conversation turn {idx} missing 'from' or 'value'")
        return {"valid": len(errors) == 0, "errors": errors}
