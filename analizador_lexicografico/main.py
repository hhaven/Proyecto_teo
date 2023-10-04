import re

# Expresiones
token_patterns = [
    (r'\/\*[\s\S]*?\*\/', 'COMMENT_MULTILINE'),  # Token para comentarios multilínea "/* ... */"
    (r'\/\/[^\n]*', 'COMMENT_LINE'),  # Token para comentarios de línea "// ..."
    (r'if', 'IF'),  # Token para la palabra clave "if"
    (r'else', 'ELSE'),  # Token para la palabra clave "else"
    (r'while', 'WHILE'),  # Token para la palabra clave "while"
    (r'int|float|char|void', 'TYPE'),  # Token para tipos de datos (int, float, char, void)
    (r'\d+\.\d+[eE][+-]?\d+', 'DOUBLE'),  # Token para números de doble precisión en notación científica
    (r'\d+\.\d+', 'FLOAT'),         # Token para números de punto flotante
    (r'\d+', 'NUM'),                # Token para números enteros
    (r'\+', 'PLUS'),  # Token para el operador de suma "+"
    (r'-', 'MINUS'),  # Token para el operador de resta "-"
    (r'\*', 'TIMES'),  # Token para el operador de multiplicación "*"
    (r'/', 'DIVIDE'),  # Token para el operador de división "/"
    (r'\(', 'LPAREN'),  # Token para el paréntesis izquierdo "("
    (r'\)', 'RPAREN'),  # Token para el paréntesis derecho ")"
    (r'\{', 'LBRACE'),  # Token para la llave izquierda "{"
    (r'\}', 'RBRACE'),  # Token para la llave derecha "}"
    (r';', 'SEMICOLON'),  # Token para el punto y coma ";"
    (r',', 'COMMA'),  # Token para la coma ","
    (r'"[^"]*"', 'STRING'), # Token para cadenas de caracteres
    (r'=', 'ASSIGN'),      # Token para  "="
    (r'\+=', 'ADD_ASSIGN'), # Token para  "+="
    (r'-=', 'SUB_ASSIGN'), # Token para  "-="
    (r'>', 'GREATER_ASSIGN'), # Token para  "-="
    (r'<', 'LESSER_ASSIGN'), # Token para  "-="
    (r'#include\s*<.*?>', 'INCLUDE'), # Token para include
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),  # Token para identificadores
]
# Expresión regular para ignorar espacios en blanco y saltos de línea
ignore_pattern = r'[ \t\n]+'

# Leer codigo
class SymbolTable:
    def __init__(self):
        self.table = {}

    def insert(self, name, token_type, value=None):
        if name not in self.table:
            self.table[name] = {'type': token_type, 'value': value}
        else:
            # Manejar colisiones si es necesario
            pass

    def lookup(self, name):
        return self.table.get(name, None)

    def delete(self, name):
        if name in self.table:
            del self.table[name]

# Crear una instancia de la tabla de símbolos
symbol_table = SymbolTable()

# Función para tokenizar y agregar a la tabla de símbolos
def tokenize_and_add_to_symbol_table(source_code, line_number):

    tokens = []
    source_code = source_code.strip()
    in_string = False

    if source_code:
        while source_code:
            for pattern, token_type in token_patterns:
                match = re.match(pattern, source_code)
                if match:
                    value = match.group(0)
                    if token_type != 'IGNORE':
                        tokens.append((token_type, value))
                        if token_type == 'ID':
                            symbol_table.insert(value, token_type)
                        elif token_type == 'NUM':
                            symbol_table.insert(value, token_type, int(value))
                        elif token_type == 'FLOAT':
                            symbol_table.insert(value, token_type, float(value))
                        elif token_type == 'STRING':
                            if in_string:
                                tokens.pop()  # Eliminar el último token (comilla de cierre)
                                value = tokens[-1][1] + value  # Concatenar la cadena
                                tokens[-1] = ('STRING', value)
                            else:
                                in_string = True
                    source_code = source_code[len(value):].strip()
                    break
            else:
                raise SyntaxError(f"Token no válido en: {source_code}")
    print (f"\n-------------------------------------------------")
    print(f"Linea #{line_number}")
    print(f"Cddigo: {line}")
    print(f"Tokens son {tokens}")

    # Propiedades de los tokens
    print(f"\nLinea #{line_number} Propiedades")
    for token_type, token_value in tokens:
        print(f"\nTipo es: {token_type}")
        print(f"Identificador: {token_value}")

# Leer código y agregar tokens a la tabla de símbolos
if __name__ == "__main__":
    file_path = "analizador_lexicografico/codigoenc.txt"

    try:
        with open(file_path, 'r') as file:
            line_number = 1
            for line in file:
                source_code = line
                tokenize_and_add_to_symbol_table(source_code, line_number)
                line_number += 1

        print (f"\n-------------------------------------------------")    
    except FileNotFoundError:
        print(f"El archivo '{file_path}' no se encontró.")