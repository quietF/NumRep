import Jama.*;

public class Test {
	
	public static void main(String[] args) {
		Distribution normal = new Distribution();
		double a = -4.;
		double b = 4.;
		Random aleatorio = new Random(a, b, normal);
		
		double[] fmax = aleatorio.findFmax();
		System.out.println(fmax[1]);
		
		System.out.println(Math.random());
		
		System.out.println(aleatorio.getRandBelow());
		
		int nIterations = 100000;
		
		//double[][] data = new double[nIterations][1];
		
		double[][] data = aleatorio.getData(nIterations);
		
		MyFileWriter fw = new MyFileWriter();
		
		Matrix A = new Matrix(data);
		
		fw.writeFile("test.txt", A);
		System.out.println("a");
	}

}
