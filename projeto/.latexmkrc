# Configuracao do latexmk para este projeto.
# Lida automaticamente pelo latexmk, independente de editor ou sistema
# operacional -- nao e preciso configurar nada no VS Code.
#
# Manda todo o lixo de compilacao (.aux, .log, .bbl, .toc...) para
# projeto/build/, que ja esta no .gitignore, e mantem o PDF final em
# projeto/documentacao-rank-ia.pdf, que e versionado.

$aux_dir  = "build";
$out_dir  = ".";
$pdf_mode = 1;
