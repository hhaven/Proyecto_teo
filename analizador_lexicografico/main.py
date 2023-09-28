import re

# Expresiones regulares para tokens
token_patterns = [
    (r'if', 'IF'),
    (r'else', 'ELSE'),
    (r'while', 'WHILE'),
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),  # Identificadores
    (r'\d+', 'NUM'),  # Números enteros
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'\{', 'LBRACE'),
    (r'\}', 'RBRACE'),
    (r';', 'SEMICOLON'),
]

# Expresión regular para ignorar espacios en blanco y saltos de línea
ignore_pattern = r'[ \t\n]+'

# Función para tokenizar el contenido de un archivo
def tokenize_file(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()
        tokens = tokenize(source_code)
    return tokens

# Función para tokenizar el código fuente
def tokenize(source_code):
    tokens = []
    source_code = source_code.strip()
    
    while source_code:
        for pattern, token_type in token_patterns:
            match = re.match(pattern, source_code)
            if match:
                value = match.group(0)
                if token_type != 'IGNORE':
                    tokens.append((token_type, value))
                source_code = source_code[len(value):].strip()
                break
        else:
            raise SyntaxError(f"Token no válido en: {source_code}")
    
    return tokens

# Ejemplo de uso: Leer desde un archivo .txt
if __name__ == "__main__":
    file_path = "codigoenc.txt"  # Reemplaza con la ruta de tu archivo .txt

    try:
        tokens = tokenize_file(file_path)
        for token in tokens:
            print(f"Token: {token[0]}, Valor: {token[1]}")
    except FileNotFoundError:
        print(f"El archivo '{file_path}' no se encontró.")




