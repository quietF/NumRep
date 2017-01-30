
public class Random {
	
	private double a = -1.;
	private double b = 1.;
	private Distribution distribution = new Distribution();
	
	public Random(double a, double b, Distribution distribution) {
		this.a = a;
		this.b = b;
		this.distribution = distribution;
	}

	public double getA() {
		return a;
	}

	public void setA(double a) {
		this.a = a;
	}

	public double getB() {
		return b;
	}

	public void setB(double b) {
		this.b = b;
	}
	
	public double findFmax(){
		double fmax = this.distribution.getYvalue(this.a), faux = fmax;
		int nIterations = 1000;
		double dx = (this.b - this.a) / nIterations;
		System.out.println(dx);
		for(int i=0; i<nIterations; i++){
			faux = this.distribution.getYvalue(this.a + i*dx);
			if(faux > fmax) fmax = faux;
		}
		return fmax;
	}
	
	

}
