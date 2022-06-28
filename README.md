# PCS3216
Sistemas de Programação (2022)

Escola Politécnica da USP

Projeto de um simulador de um sistema de programação simples, funcional e completo.

Alunos:
* Alessandro Jiã Iong Li - 10291791        
* Gustavo Freitas de Sá Oliveira - 11261062
* Roberta Boaventura Andrade - 11260832

--------------------

### Documentos relevantes

* Enunciado do projeto: https://edisciplinas.usp.br/pluginfile.php/7059383/mod_resource/content/1/PCS%203216%20-%20Projeto%202022.pdf

--------------------

### Especificações da máquina virtual

A máquina virtual projetada para o projeto possui:

#### Registradores

* Program Counter (16 bits): armazena o endereço da instrução que está sendo executada.

* Link Register (16 bits): armazena o endereço de retorno em entradas de sub-rotina.

* Instruction Register (16 bits): armazena o código binário da instrução atual a ser executada.

* Accumulator (8 bits): registrador de propósito geral, à disposição do programador.

#### Memória

* 16 bancos (identificados de 0x0 até 0xF) de memória, com 4096 bytes (endereços de 0x000 até 0xFFF) cada.

#### Programas de sistema

* Loader: lê um arquivo contendo uma imagem carregável, e a armazena na posição de memória correspondente.

* Dumper: lê uma região de memória e gera um arquivo contendo uma imagem carregável, pronta para ser carregada por um loader.

* Assembler: lê um arquivo contendo código fonte em linguagem mnemônica, e gera um arquivo contendo código objeto em linguagem de máquina, pronto para ser carregado por um loader.

* Linker: liga entry-points entre programas, armazenando endereços numa tabela de símbolos. Permite que programas possam chamar uns aos outros através resolução de endereços externos.

--------------------

### Linguagem mnemônica

A máquina virtual é capaz de montar programas em linguagem simbólica. Para isso, foi definida uma linguagem a nível de montagem, com 16 instruções no total, opcodes de 4 bits e instruções de 2 bytes.

#### Instruções

* `JP` JUMP - causa um salto incondicional para o endereço de destino.
    * Estrutura:
        * `[15:12]` => opcode
        * `[11:0]` => operando

* `JZ` JUMP IF ZERO - causa um salto para o endereço de destino se o conteúdo no acumulador for nulo.
    * Estrutura:
        * `[15:12]` => opcode
        * `[11:0]` => operando

* `JN` JUMP IF NEGATIVE - causa um salto para o endereço de destino se o conteúdo no acumulador for negativo.
    * Estrutura:
        * `[15:12]` => opcode
        * `[11:0]` => operando

* `LV` LOAD VALUE - carrega um valor imediato no acumulador.
    * Estrutura:
        * `[15:12]` => opcode
        * `[7:0]  `=> operando

* `+` ADD - soma um valor armazenado na memória com o acumulador, e armazena o resultado no acumulador.
    * Estrutura:
        * `[15:12]` => opcode
        * `[11:0]` => operando

* `-` SUBTRACT - subtrai um valor armazenado na memória do acumulador, e armazena o resultado no acumulador.
    * Estrutura:
        * `[15:12]` => opcode
        * `[11:0]` => operando

* `*` MULTIPLY - multiplica o acumulador por um valor armazenado na memória, e armazena o resultado no acumulador.
    * Estrutura:
        * `[15:12]` => opcode
        * `[11:0]` => operando

* `/` DIVIDE - divide o acumulador por um valor armazenado na memória, e armazena o resultado no acumulador.
    * Estrutura:
        * `[15:12]` => opcode
        * `[11:0]` => operando

* `LD` LOAD - carrega o acumulador com um valor armazenado na memória.
    * Estrutura:
        * `[15:12]` => opcode
        * `[11:0]` => operando

* `MM` MOVE TO MEMORY - escreve num endereço de memória o valor do acumulador.
    * Estrutura:
        * `[15:12]` => opcode
        * `[11:0]` => operando

* `SC` SUBROUTINE CALL - escreve o valor do program counter no link register, e desvia incondicionalmente.
    * Estrutura:
        * `[15:12]` => opcode
        * `[11:0]` => operando

* `RS` RETURN FROM SUBROUTINE - escreve o valor do link register no program counter.
    * Estrutura:
        * `[15:12]` => opcode

* `HM` HALT MACHINE - causa um halt na máquina, ou muda o modo de endereçamento na memória.
    * Estrutura:
        * `[15:12]` => opcode
        * `[3:0]` => operando

    * Operando:
        * `0000` => Causa um halt na máquina.
        * `0001` => Liga o modo de endereçamento indireto.
        * `0010` => Desliga o modo de endereçamento indireto.

* `GD` GET DATA - pede para que o usuário entre com um dado, que é inserido no acumulador.
    * Estrutura:
        * `[15:12]` => opcode

* `PD` PUT DATA - imprime na tela o dado do acumulador.
    * Estrutura:
        * `[15:12]` => opcode
        * `[3:0]` => operando

    * Operando:
        * `0000` => Imprime o dado em formato decimal.
        * `0001` => Imprime o dado em formato binário.
        * `0010` => Imprime o dado em formato hexadecimal.
        * `0011` => Imprime o dado em formato unicode.

* `OS` OPERATING SYSTEM - imprime na tela o estado atual da máquina, ou encerra a execução do progama.
    * Estrutura:
        * `[15:12]` => opcode
        * `[3:0]` => operando

    * Operando:
        * `0000` => Imprime na tela o atual estado da máquina.
        * `1111` => Interrompe a execução do programa.

#### Pseudo-instruções

* `<` EXT - indica ao ligador que um label é um entry point externo ao programa.

* `>` ENT - indica ao ligador que um label é um entry point interno ao programa.

* `@` ORG - indica ao montador o endereço absoluto de origem do código a seguir.
    * Operador:
        * `[15:12]` => banco de memória do código a seguir.
        * `[11:0]` => endereço inicial do código a seguir.

* `K` BYTE - preenche um byte com um valor imediato na memória.
    * Operador:
        * `[15:0]`=> valor a ser preenchido.

* `$` SPACE - reserva uma sequência de bytes nulos de memória.
    * Operador:
        * `[15:0]`=> número de bytes nulos a serem reservados.

* `#` END - indica ao montador o final físico do programa.

#### Sintaxe da linguagem

Para a construção de programas e declaração de dados em linguagem simbólica, é possível utilizar qualquer editor de texto. Para isso, é suficiente salvar o arquivo `.asm` contendo o código fonte em linguagem mnemônica no diretório `.\source\`.

Os códigos na linguagem mnemônica definida são compostos de:

* Cabeçalho: onde são identificados os entry-points externos e internos do programa. Nesse trecho, devem ser utilizadas apenas pseudo-instruções dos tipos `<` e `>`. Essa parte é ignorada pelo montador, mas as suas informações são úteis para o ligador, que conecta trechos de código entre os programas já montados. Esse trecho é opcional.

* Endereço de origem: onde é identificado o endereço de origem absoluto do programa. Nesse trecho, devem ser utilizadas apenas pseudo-instruções do tipo `@`.

* Código: onde é feita a sequencialização das instruções ou declaração de dados. Nesse trecho, podem ser utilizadas quaisquer instruções ou pseudo-instruções que não são utilizados em outros trechos do código.

* Final físico: onde é identificado o final do programa. Nesse trecho, devem ser utilizadas apenas a pseudo-instrução do tipo `#`. Ao encontrar essa instrução, o montador insere uma chamada de sistema operacional (instrução do tipo `OS`) que causa a interrupção da execução de código.

As instruções e pseudo-instruções são compostas de:

* Label: opcional. Indica o nome de uma instrução, e pode ser referenciada em outros pontos do programa ou como entry-points.

* Comando: obrigatório. Indica qual a instrução ou pseudo-instrução executada, e deve ser um dos mnemônicos listados acima. Linhas sem comandos serão ignoradas pelos programas de sistema.

* Operador: opcional. Embora a maioria da instrução possua um operador, é possível deixá-lo em branco. Nesse caso, o montador irá utilizar o valor 0x0 por padrão.

* Comentário: opcional. Qualquer texto que seja encontrado numa linha de código depois do caracter `;` é considerado um comentário, e será totalmente ignorado pelos programas de sistema.

Ao final desse documento, serão apresentados exemplos de código e utilização da máquina.

--------------------

### Interpretador de comandos

A interação entre o operador da máquina e o fluxo de dados interno é dado por meio de uma interface guiada por comandos.

#### Comandos disponíveis

* `$ HELP` imprime uma descrição detalhada dos possíveis comandos.
    * Sintaxe:
        `$ HELP`

* `$ DIR` imprime os nomes dos arquivos disponíveis para `ASM` e `LOAD`.
    * Sintaxe:
        `$ DIR`

* `$ STA` imprime o estado atual dos registradores da máquina virtual.
    * Sintaxe:
        `$ STA`

* `$ ASM` monta um arquivo com código em linguagem mnemônica, gerando um arquivo com código objeto em linguagem de máquina pronto para ser carregado. Faz também a ligação com entry-points externos e atualiza a tabela de endereços do ligador.
    * Sintaxe:
        `$ ASM FILENAME`

* `$ LOAD` carrega uma imagem carregável de memória.
    * Sintaxe:
        `$ LOAD FILENAME`

* `$ DUMP` descarrega uma imagem carregável de memória, pronta pra ser carregada pelo loader.
    * Sintaxe:
        `$ DUMP FILENAME [-s SIZE] [-a ADRESS] [-b BANK] [--hex]`
    * Opções:
        * `-s` seleciona o tamanho em bytes de memória a ser descarregada. O valor é de 16 por padrão.
        * `-a` seleciona o endereço inicial de memória a ser descarregado. O valor é de 0x0 por padrão.
        * `-b` seleciona o banco de memória a ser descarregado. O valor é de 0x0 por padrão.
        * `--hex` seleciona se o dumper acionado deve escrever a região de memória em imagem carregável (dumper absoluto) ou em tela (dumper hexadecimal).

* `$ RUN` roda código em linguagem de máquina presente numa posição de memória.
    * Sintaxe:
        `$ RUN [-a ADRESS] [-b BANK] [--step]`
    * Opções:
        * `-a` seleciona o endereço inicial de memória do código a ser rodado. O valor é de 0x0 por padrão.
        * `-b` seleciona o banco de memória que contém o código a ser rodado. O valor é de 0x0 por padrão.
        * `--step` seleciona se o código deve ser rodado passo-a-passo. Por padrão, o código é rodado de uma vez.

* `$ EXIT` sai do interpretador de comandos e finaliza o programa.
    * Sintaxe:
        `$ EXIT`

--------------------

### Exemplos de código e utilização da máquina

Para explicar o funcionamento da linguagem simbólica e da máquina virtual com mais detalhes, serão apresentados códigos exemplo, construídos na linguagem de montagem definida anteriormente.

* `hello.asm`

Primeiramente, será apresentado o programa mais simples de qualquer linguagem de programação, o "Hello, world!"

Nesse programa, possuímos como objetivo a impressão ao usuário da frase "Hello, world!".

Como esse programa não se utilizado de endereços externos, não é necessária a adição do cabeçalho. O programa, então, é iniciado com o endereço de origem do código. É adicionada também uma instrução de `JP`, para indicar que o código deve ser iniciado na label `START`.

```
; Hello
; *********
; Programa que realiza a impressão da frase "Hello, world!".

            @       /0000           ; endereço inicial do código na memória
            JP      START           ; iniciando a execução do programa
```

São declarados os dados da string em bytes em formato unicode. O zero demarca o fim da string.

```
STRING      K       =72             ; declaração da string, em formato unicode
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
```

Em seguida, é feito um loop na string, utilizando a instrução `PD` para imprimir os dados na tela. Quando o valor presente no acumulador é nulo, o programa entende que foi alcançado o fim da string e desvia para o final do programa, na label `END`.

```
ONE         K       =1
ADDR        K       =0
CURR        K       =2              ; endereço de acesso atual

START       LV      =0
            HM      /01             ; ligando o modo de endereçamento indireto
            LD      ADDR            ; carregando o caracter atual
            JZ      END             ; se zero, ir para END
            PD      =3              ; imprimir dado em formato unicode
            LD      CURR            ; incrementando CURR
            +       ONE
            MM      CURR
            JP      START           ; loop

END         LV      =2              ; voltando ao estado original
            MM      CURR
            #                       ; fim do programa
```

Para executar esse programa na máquina virtual, basta seguir a seguinte sequência de comandos:

```
Enter a command! Type HELP to see possible commands.
$ ASM hello  
$ LOAD hello
$ RUN -a 0 -b 0
ACC => H
ACC => e
ACC => l
ACC => l
ACC => o
ACC => ,
ACC =>  
ACC => w
ACC => o
ACC => r
ACC => l
ACC => d
ACC => !
$
```

O comando `ASM` serve para montar o programa em linguagem simbólica e gerar o arquivo `hello.obj`, uma imagem carregável de memória dentro da pasta de códigos objetos executáveis. O comando `LOAD` faz a carga do conteúdo dessa imagem na memória da máquina, e o comando `RUN` faz a interpretação e execução das instruções binárias presentes na memória da máquina. Com os comandos acima executados, para um exemplo de utilização do dumper hexadecimal, pode-se usar:

```
$ DUMP -a 0 -b 0 --hex 
Memory bank: 00
000 => 00
001 => 13
002 => 48
003 => 65
004 => 6C
005 => 6C
006 => 6F
007 => 2C
008 => 20
009 => 77
00A => 6F
00B => 72
00C => 6C
00D => 64
00E => 21
00F => 00
$
```

Pela resposta da máquina, percebe-se que o dumper hexadecimal exibe na tela os conteúdos das posições de memória que foram carregadas pelo loader.

Pode-se também utilizar o dumper absoluto:

```
DUMP hellodump -a 0 -b 0
```

Esse comando gera a imagem carregável `hellodump.obj` no diretório `.\obj\`. Como esperado, os dois primeiros bytes desse arquivo são indicadores do banco e endereço que o código deve começar a ser armazenado na memória. Podemos visualizar o arquivo:

```
0000000000000000
00000000
00010011
01001000
01100101
01101100
01101100
01101111
00101100
00100000
01110111
01101111
01110010
01101100
01100100
00100001
00000000
```

Esse arquivo contém código objeto em linguagem de máquina, pronta para ser carregada por um loader. Para o teste dessa interação, pode ser rodado:

```
LOAD hellodump
```

Nenhum erro será exibido, e o código será carregado na memória da máquina na mesma região que foi anteriormente decarregada. Uma vez que o código carregado é o mesmo que foi descarregado e suas posições alvo de memória são idênticas, não há mudanças perceptíveis no estado dos registradores e memória da máquina.

* `somador.asm` e `soma.asm`

Agora, será apresentado um exemplo mais complexo, que faz o uso do ligador para executar códigos em arquivos separados.

A sub-rotina `SOMADOR` faz o uso de entry-points para realizar a soma de dois valores armazenados na memória. Ao final da sub-rotina, a instrução `RS` é utilizada para retornar o program counter para o fluxo principal, visto que esse registrador foi salvo no link register.

```
; Somador
; *********
; Subrotina que realiza uma soma de dois valores na memória, e deposita o resultado no acumulador.

SOMADOR     >                       ; cabeçalho - definindo entry-points
ENTRADA1    >
ENTRADA2    >

            @       /00FF           ; endereço inicial do código na memória
            JP      SOMADOR
ENTRADA1    K       =0              ; valor 1 a somar
ENTRADA2    K       =0              ; valor 2 a somar
SOMADOR     LD      ENTRADA1        ; realizando a soma
            +       ENTRADA2
            RS                      ; retornando da sub-rotina
```

O programa `SOMA` testa a chamada do `SOMADOR`, visto que os entry-points externos utilizados na sub-rotina são resolvidos pelo ligador. As variáveis são primeiramente passadas na memória, e logo a sub-rotina é chamada.

```
; Soma
; *********
; Programa principal que chama o somador.

SOMADOR     <                       ; cabeçalho - definindo entry-points
ENTRADA1    <
ENTRADA2    <
SAIDA       >

            @       /0000           ; endereço inicial do código na memória
            JP      INICIO
VALOR1      K       =50             ; valor 1 a somar
VALOR2      K       #101101         ; valor 2 a somar
SAIDA       K       /0000           ; endereço de salvamento da soma
INICIO      LD      VALOR1          ; passando as variáveis na memória
            MM      ENTRADA1
            LD      VALOR2
            MM      ENTRADA2
            SC      SOMADOR         ; chamando o somador
            PD      =0              ; exibindo dados na tela
            #                       ; fim do programa
```

Para executar esse programa na máquina virtual, basta seguir a seguinte sequência de comandos:

```
Enter a command! Type HELP to see possible commands.
$ ASM somador
$ LOAD somador
$ ASM soma
$ LOAD soma
$ RUN -a 0 -b 0
ACC => 095
$
```

Pela resposta da máquina, percebe-se que a soma foi defidamente executada e o resultado foi armazenado no acumulador. Assim, comprova-se o correto funcionamento das chamadas de sub-rotina.
