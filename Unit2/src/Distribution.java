
public class Distribution {
	
	private double a=0., b=100.;
	private double mu=0., sd=1.;

	public Distribution(double a, double b, double mu, double sd) {
		this.a = a;
		this.b = b;
		this.mu = mu;
		this.sd = sd;
	}

	public double getA() { return a;}

	public void setA(double a) { this.a = a;}

	public double getB() { return b;}

	public void setB(double b) { this.b = b;}
	
	public double getMU() { return mu;}

	public void setMU(double mu) { this.mu = mu;}

	public double getSD() { return sd;}

	public void setSD(double sd) { this.sd = sd;}
	
	public double getNormalDist(double x){
		return Math.exp(-(x-mu)*(x-mu)/(2 * sd * sd));
	}
	
	public double generateRand(){
		return a + (b - a) * Math.random();
	}
	
	public double[] generateNormalData(int nIterations){
		double[] randomData = new double[nIterations];
		for(int i=0; i<nIterations; i++){
			double x = generateRand();
			randomData[i] = getNormalDist(x);
		}
		return randomData;
	}

}
