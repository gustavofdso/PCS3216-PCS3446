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

A máquina virtual projetada para a elaboração do projeto possui:

#### Registradores

* Program Counter       (16 bits): armazena o endereço que está sendo executada.

* Link Register         (16 bits): armazena o endereço de retorno numa entrada de sub-rotina.

* Instruction Register  (16 bits): armazena o código binário atual.

* Accumulator            (8 bits): registrador de propósito geral, à disposição do programador.

#### Memória

* 16 bancos (0x0 até 0xF) de memória, de 4096 (0x000 até 0xFFF) bytes cada.

#### Programas de sistema

* Loader: lê um arquivo contendo código objeto em linguagem de máquina, e armazena esse código na posição de memória correspondente.

* Dumper: lê uma região de memória e gera um arquivo contendo código objeto em linguagem de máquina, pronto pra ser carregado por um loader.

* Assembler: lê um arquivo contendo código fonte em linguagem mnemônica, e gera um arquivo contendo código objeto em linguagem de máquina, pronto pra ser carregado por um loader.

* Linker: liga entry-points entre programas, armazenando endereços numa tabela de símbolos. Faz a ligação entre os programas, fazendo com que programas possam chamar uns aos outros.

--------------------

### Linguagem mnemônica

A máquina virtual é capaz de montar programas em linguagem simbólica. Para isso, foi definida uma linguagem a nível de montagem, com opcodes de 4 bits e 16 instruções no total:

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

* `OS` OPERATING SYSTEM - imprime na tela o atual estado da máquina, ou encerra a execução do progama.
    * Estrutura:
        * `[15:12]` => opcode
        * `[3:0]` => operando

    * Operando:
        * `0000` => Imprime na tela o atual estado da máquina.
        * `1111` => Interrompe a execução do programa.

#### Pseudo-instruções

* `<` EXT - indica que um label é um entry point externo ao programa ao ligador.

* `>` ENT - indica que um label é um entry point interno ao programa ao ligador.

* `@` ORG - indica o endereço absoluto de origem ao montador.
    * Operador:
        * `[15:12]` => banco de memória do código seguinte.
        * `[11:0]` => endereço inicial do código seguinte.

* `K` BYTE - reserva um byte de memória com um imediato.
    * Operador:
        * `[15:0]`=> imediato a ser carregado.

* `$` SPACE - reserva um número de bytes nulos de memória.
    * Operador:
        * `[15:0]`=> número de bytes nulos que devem ser reservados.

* `#` END - indica o final físico do código a ser montado.

#### Sintaxe da linguagem

Para a construção de programas e declaração de dados na linguagem simbólica, é possível utilizar qualquer editor de texto.

Os códigos na linguagem mnemônica definida são compostos de:

* Cabeçalho: são identificados os entry-points externos e internos do programa. Nesse trecho, devem ser utilizadas apenas pseudo-instruções dos tipos `<` e `>`. Essa parte é ignorada pelo montador, mas as suas informações são úteis para o ligador, que conecta trechos de código entre os programas já montados. Esse trecho é opcional.

* Endereço de origem: é identificado o endereço de origem absoluto do programa. Nesse trecho, devem ser utilizadas apenas pseudo-instruções do tipo `@`.

* Código: é feita a sequencialização das instruções ou declaração de dados. Nesse trecho, podem ser utilizadas quaisquer instruções ou pseudo-instruções que não são utilizados em outros trechos do código.

* Final físico: é identificado o final físico do programa. Nesse trecho, devem ser utilizadas apenas pseudo-instruções do tipo `#`. Ao encontrar essa instrução, o montador para a montagem e insere uma chamada de sistema operacional (instrução do tipo `OS`) que causa a interrupção da execução de código.

As instruções e pseudo-instruções devem seguir o seguinte padrão:



#### Exemplos



--------------------

### Interpretador de comandos

A interação entre o operador da máquina e o fluxo de dados interno é dado por meio de uma interface guiada por comandos.

#### Comandos disponíveis

* `$ HELP` imprime uma descrição dos possíveis comandos.
    * Sintaxe:
        `$ HELP`

* `$ DIR` imprime os nomes dos arquivos disponíveis para ASM e LOAD.
    * Sintaxe:
        `$ DIR`

* `$ ASM` monta um arquivo com código em linguagem mnemônica, gerando um arquivo com código em linguagem de máquina pronto para ser carregado. Faz a ligação com entry-points externos e atualiza a tabela de entry-points do ligador.
    * Sintaxe:
        `$ ASM FILENAME`

* `$ LOAD` carrega um arquivo com código em linguagem de máquina na memória.
    * Sintaxe:
        `$ LOAD FILENAME`

* `$ DUMP` carrega um arquivo com código em linguagem de máquina na memória.
    * Sintaxe:
        `$ DUMP FILENAME [-s SIZE] [-a ADRESS] [-b BANK] [--hex]`
    * Opções:
        * `-s` seleciona o tamanho em bytes de memória a ser descarregada. O valor é de 16 por padrão.
        * `-a` seleciona o endereço inicial de memória a ser descarregado. O valor é de 0x0 por padrão.
        * `-b` seleciona o banco de memória a ser descarregado. O valor é de 0x0 por padrão.
        * `--hex` seleciona se a memória deve ser emitido num arquivo ou impresso na tela. Por padrão, a memória é emitida num arquivo.

* `$ RUN` roda código binário numa posição de memória.
    * Sintaxe:
        `$ RUN [-a ADRESS] [-b BANK] [--step]`
    * Opções:
        * `-a` seleciona o endereço inicial de memória do código a ser rodado. O valor é de 0x0 por padrão.
        * `-b` seleciona o banco de memória do código a ser rodado. O valor é de 0x0 por padrão.
        * `--step` seleciona se o código deve ser rodado passo-a-passo. Por padrão, o código é rodado de uma vez.

* `$ EXIT` sai do interpretador de comandos e finaliza o programa.
    * Sintaxe:
        `$ EXIT`

#### Como utilizar a máquina

