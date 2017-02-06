import Jama.Matrix;

public class MCsim {
	
	private double a = 0.;
	private double b = 1.;
	private double tau = 2.2;
	private double[] distMax = new double[2];
	
	public MCsim(double a, double b) {
		this.a = a;
		this.b = b;
		this.distMax = this.findFmax();
	}
	
	public double evaluateDist(double ti){ return Math.exp(- ti / tau) / tau;}
	
	public double[] findFmax(){
		double fmax = this.evaluateDist(this.a), faux = fmax,
				tmax = this.a;
		int nIterations = 1000;
		double dx = (this.b - this.a) / nIterations;
		for(int i=0; i<nIterations; i++){
			faux = this.evaluateDist(this.a + i*dx);
			if(faux > fmax){
				fmax = faux;
				tmax = this.a + i*dx;
			}
		}
		return new double[]{tmax, fmax};
	}
	
	public double getRandBelow(){
		double randNumber = this.a + (this.b - this.a) * Math.random();
		double y1 = this.evaluateDist(randNumber);
		double y2 = Math.random() * this.distMax[1];
		if(y2 < y1) return randNumber;
		else return this.getRandBelow();
	}
	
	public double[][] getnRandBelow(int n){
		double[][] nrand = new double[n][1];
		for(int i=0; i<n; i++)
			nrand[i][0] = this.getRandBelow();
		return nrand;
	}
	
	public void writeToFile(String outFile, int nIterations){
		
		double[][] data;
		data = this.getnRandBelow(nIterations);
		MyFileWriter fw = new MyFileWriter();
		Matrix A = new Matrix(data);
		fw.writeFile(outFile, A);
	}
	
	public double integralInterval(double min, double max, int nPoints){
		MCsim sub_montecarlo = new MCsim(min, max);
		double top = 1.001 * sub_montecarlo.distMax[1];
		double totalArea = top * (max -min);
		int pointsIn = 0;
		double[] coords = new double[2];
		for(int i=0 ;i<nPoints; i++){
			coords[0] = min + (max - min) * Math.random();
			coords[1] = top * Math.random();
			if(coords[1] <= sub_montecarlo.evaluateDist(coords[0])) 
				pointsIn += 1;
		}
		return totalArea * pointsIn/(double)nPoints;
	}
	
	public double integralNumeric(double min, double max, int nPoints){
		int nDivisions = 10;
		double ans = 0.;
		for(int i=0; i<nDivisions; i++){
			ans += this.integralInterval(min + i*(max-min)/nDivisions, 
					min + (i+1)*(max-min)/nDivisions, nPoints);
		}
		
		return ans;
	}
	
	public double avgTau(int n){
		/*
		 * return the average value of tau for one simulation that
		 * is created with n data points.
		 */
		double avgTau = 0.;
		for(int i=0; i<n; i++) avgTau += this.getRandBelow() / (double)n;
		return avgTau;
	}
	
	public double[][] estimateTau(int nSets, int n){
		/*
		 * return a matrix of nSets of average values of tau generated
		 * from simulations of n data points.
		 */
		double[][] tauish = new double[nSets][1];
		for(int i=0; i<nSets; i++) 
			tauish[i][0] = this.avgTau(n);
		return tauish;
	}
	
	public void writeToFileTauData(String outFile, int nSets, int nIterations){
		/*
		 * Write nSets of averaged tau values obtained from nIterations
		 * of random number simulations to the outFile.
		 * This is then plotted with: python3 MyPlot.py outFile
		 */
		double[][] data = this.estimateTau(nSets, nIterations);
		MyFileWriter fw = new MyFileWriter();
		Matrix A = new Matrix(data);
		fw.writeFile(outFile, A);
	}
	
	public static void main(String[] args) {
		
		MCsim montecarlo = new MCsim(0, 15.);
		int nIterations = 1000;
		montecarlo.writeToFile("mc_trial.txt", nIterations);
		int nSets = 500;
		montecarlo.writeToFileTauData("tau_data.txt", nSets, nIterations);
		//int nPoints = 100000;
		//System.out.println("The numerical integral is: " + 
				//montecarlo.integralNumeric(0., 1., nPoints));
	}

}
