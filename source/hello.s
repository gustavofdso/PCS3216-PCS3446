; Hello
; *********
; Programa que realiza a impressão da frase "Hello, world!".

            @       /0000           ; endereço inicial do código na memória
            JP      START           ; iniciando a execução do programa

STRING      K       =72             ; declaração da string, em formato ASCII
            K       =101
            K       =108
            K       =108
            K       =111
            K       =44
            K       =32
            K       =119
            K       =111
            K       =114
            K       =108
            K       =100
            K       =33
            K       =0

ONE         K       =1
ADDR        K       =0
CURR        K       =2              ; endereço de acesso atual

START       LV      =0
            HM      /01             ; ligando o modo de endereçamento indireto
            LD      ADDR            ; carregando o caracter atual
            JZ      END             ; se zero, ir para END
            PD      =3              ; imprimir dado em formato ASCII
            LD      CURR            ; incrementando CURR
            +       ONE
            MM      CURR
            JP      START           ; loop

END         LV      =2              ; voltando ao estado original
            MM      CURR
            #                       ; fim do programa