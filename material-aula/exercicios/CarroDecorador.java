interface ICarro {
    String getDescricao();
    double getPreco();
}

class CarroBase implements ICarro {
    public String getDescricao() {
        return "Carro";
    }

    public double getPreco() {
        return 50000.0;
    }
}

abstract class DecoradorCarro implements ICarro {
    protected ICarro componente;

    public DecoradorCarro(ICarro componente) {
        this.componente = componente;
    }

    public String getDescricao() {
        return componente.getDescricao();
    }

    public double getPreco() {
        return componente.getPreco();
    }
}

class OpcionalNavegacao extends DecoradorCarro {
    public OpcionalNavegacao(ICarro componente) {
        super(componente);
    }

    public String getDescricao() {
        return componente.getDescricao() + " + Navegação";
    }

    public double getPreco() {
        return componente.getPreco() + 2500.0;
    }
}

class OpcionalCor extends DecoradorCarro {
    private String nomeCor;

    public OpcionalCor(ICarro componente, String nomeCor) {
        super(componente);
        this.nomeCor = nomeCor;
    }

    public String getDescricao() {
        return componente.getDescricao() + " + Cor " + nomeCor;
    }

    public double getPreco() {
        return componente.getPreco() + 1800.0;
    }
}

public class CarroDecorador {
    public static void main(String[] args) {

        ICarro pedido1 = new CarroBase();
        pedido1 = new OpcionalNavegacao(pedido1);
        pedido1 = new OpcionalCor(pedido1, "Azul");

        System.out.println("=== Cliente 1: Carro com Navegação e Cor Azul ===");
        System.out.println("Descrição: " + pedido1.getDescricao());
        System.out.println("Preço: R$ " + pedido1.getPreco());

        System.out.println();

        ICarro pedido2 = new CarroBase();
        pedido2 = new OpcionalCor(pedido2, "Azul");

        System.out.println("=== Cliente 2: Carro apenas com Cor Azul (sem Navegação) ===");
        System.out.println("Descrição: " + pedido2.getDescricao());
        System.out.println("Preço: R$ " + pedido2.getPreco());

        System.out.println();

        ICarro pedido3 = new CarroBase();

        System.out.println("=== Cliente 3: Carro simples (sem opcionais) ===");
        System.out.println("Descrição: " + pedido3.getDescricao());
        System.out.println("Preço: R$ " + pedido3.getPreco());
    }
}