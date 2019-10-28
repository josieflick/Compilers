# Compilers
C- recursive descent parser

Lexical Analyzer
The lexer scans the input file and outputs a list of tokens. Block and line comments are stripped.

Parser
The parser was designed as a backtracking parser to avoid fixing the c- grammar. The program receives the output of the lexer as its input file. The parser throws an error if the next token is not the expected token.

