            @       /00
            JP      INICIO
VALOR1      K       =50         ; valor 1 a somar
VALOR2      K       =4          ; valor 2 a somar
GUARDAR     $       =1          ; endereco a ser guardado
INICIO      LD      VALOR1      ; passando as variáveis
            +       VALOR2
            MM      GUARDAR
            OS      /00
            #