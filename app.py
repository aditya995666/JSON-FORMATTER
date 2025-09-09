from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Dictionary of known error suggestions
error_suggestions = {
    "Expecting property name enclosed in double quotes":
        " Tip: Keys (like 'name') must use double quotes → use \"name\" not 'name'.",

    "Expecting ',' delimiter":
        "Tip: Missing comma between items. Check if a comma is missing before this line.",

    "Extra data":
        "Tip: More than one JSON object found. JSON must start and end with exactly one object or array.",

    "Unterminated string starting at":
        "Tip: String not closed. Ensure all strings have matching starting and ending quotes.",

    "Invalid control character":
        "Tip: Use proper escaping for special characters like \\n, \\t, etc. inside strings.",

    "Expecting ':' delimiter":
        " Tip: Missing colon between key and value → use \"key\": \"value\" format."
}

def validate_json(json_string):
    try:
        json.loads(json_string)
        return {
            "valid": True,
            "message": " JSON is valid!"
        }
    except json.JSONDecodeError as e:
        suggestion = " General JSON syntax error. Please double-check the structure."
        for error_msg, tip in error_suggestions.items():
            if error_msg in e.msg:
                suggestion = tip
                break

        return {
            "valid": False,
            "error": {
                "line": e.lineno,
                "column": e.colno,
                "reason": e.msg,
                "suggestion": suggestion
            }
        }

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    if not data or "json_text" not in data:
        return jsonify({"error": "Missing 'json_text' in request body"}), 400
    
    result = validate_json(data["json_text"])
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
