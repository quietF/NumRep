/**
 * @author Andres Cathey
 * @category Unit2
 *
 */


public class Random {
	
	public static void main(String[] args) {
		
		double a = -2., b = 2.;
		double mu = 0., sd = 1.;
		Distribution Normal = new Distribution(a, b, mu, sd);
		
		int nPoints = 1000;
		double[] normalPoints = Normal.generateNormalData(nPoints);
		
		for(int i=0; i<nPoints; i++)
			System.out.println(normalPoints[i]);
	}

}
