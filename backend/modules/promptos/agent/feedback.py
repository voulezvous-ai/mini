def styled_response(result: dict):
    if result.get("success"):
        return {"status": "✅ Feito", "message": result.get("message", "")}
    else:
        return {"status": "⚠️ Falhou", "message": result.get("message", "Ocorreu um erro.")}