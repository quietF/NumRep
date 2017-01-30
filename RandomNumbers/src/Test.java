
public class Test {
	
	public static void main(String[] args) {
		Distribution normal = new Distribution();
		double a = -1.;
		double b = 1.;
		Random aleatorio = new Random(a, b, normal);
		
		aleatorio.findFmax();
	}

}
