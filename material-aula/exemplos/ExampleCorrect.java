class A {
    private void f(B b) {
        int total = b.getTotal(); // A depende da interface de B, não do arquivo
    }
}

class B {
    private int total;

    public int getTotal() {
        return total;
    }

    private void g() {
        // computa total
        File arq = File.open("arq1.db");
        arq.writeInt(total);
        arq.close();
    }
}