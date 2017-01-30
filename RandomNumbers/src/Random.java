
public class Random {
	
	private double a = -1.;
	private double b = 1.;
	private Distribution distribution = new Distribution();
	private double[] distMax = new double[2];
	
	public Random(double a, double b, Distribution distribution) {
		this.a = a;
		this.b = b;
		this.distribution = distribution;
		this.distMax = this.findFmax();
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
	
	public double[] findFmax(){
		double fmax = this.distribution.getYvalue(this.a), faux = fmax,
				xmax = this.a;
		int nIterations = 1000;
		double dx = (this.b - this.a) / nIterations;
		System.out.println(dx);
		for(int i=0; i<nIterations; i++){
			faux = this.distribution.getYvalue(this.a + i*dx);
			if(faux > fmax){
				fmax = faux;
				xmax = this.a + i*dx;
			}
		}
		return new double[]{xmax, fmax};
	}
	
	public double getRandBelow(){
		double randNumber = this.a + (this.b - this.a) * Math.random();
		double y1 = this.distribution.getYvalue(randNumber);
		double y2 = Math.random() * this.distMax[1];
		if(y2 < y1) return randNumber;
		else return this.getRandBelow();
	}
	
	public double[][] getData(int nIterations){
		
		double[][] data = new double[nIterations][1];
		for(int i=0; i<nIterations; i++) data[i][0] = this.getRandBelow();
		return data;
	}

}