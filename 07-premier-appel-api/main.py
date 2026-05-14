"""
Mon premier appel API Anthropic.
Posons une question à Claude et affichons la réponse.
"""
import anthropic

# Le client lit automatiquement ANTHROPIC_API_KEY dans l'environnement
client = anthropic.Anthropic()

# La question qu'on pose à Claude
question = "Explique-moi en 3 phrases ce qu'est une API, à un médecin de 50 ans."

# L'appel — c'est ici que la magie se passe
reponse = client.messages.create(
    model="claude-haiku-4-5-20251001",  # modèle le moins cher pour démarrer
    max_tokens=300,                      # limite la longueur de la réponse
    messages=[
        {"role": "user", "content": question}
    ]
)

# Affiche la réponse
print("=== Question ===")
print(question)
print()
print("=== Réponse de Claude ===")
print(reponse.content[0].text)
print()

# Trace le coût (Haiku 4.5 = $1/MTok input, $5/MTok output)
cout = (reponse.usage.input_tokens * 1.0 + reponse.usage.output_tokens * 5.0) / 1_000_000
print(f"=== Coût ===")
print(f"Input : {reponse.usage.input_tokens} tokens")
print(f"Output : {reponse.usage.output_tokens} tokens")
print(f"Total : {cout:.6f} $ (environ {cout * 10:.4f} MAD)")
