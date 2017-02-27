import Jama.Matrix;

public class Efield {
	/*
	 * Maxwell's 1st equation (1D) with a given charge distribution.
	 * 
	 * dE(x)/dx = rho(x)
	 * 
	 * 1 - Euler integration.
	 * 2 - Runge-Kutta 2.
	 * 3 - Runge-Kutta 4.   
	 */
	
	private final double Ex0 = 0., Vx0=0.; // Boundary Condition.
	private final double x_min = 0., x_max = 4.;
	private int n = 10;
	private int order = 1;
	private double dx = (x_max-x_min)/(double)n;

	
	
	public Efield(int n, int order){
		this.n = n;
		this.order = order;
		dx = (x_max-x_min)/(double)n;
	}
	
	public double getEuler(double[][] E_or_V, int i, double dx, Function fxy){
		if(fxy.getCharge())
			return E_or_V[i-1][1] + dx * fxy.evaluate(E_or_V[i-1][0], E_or_V[i][1]);
		else
			return E_or_V[i-1][1] + dx * fxy.evaluate(2*i);
	}
	
	public double getRK2(double[][] E_or_V, int i, double dx, Function fxy){
		if(fxy.getCharge()){
			double ymid = E_or_V[i-1][1] + dx * fxy.evaluate(E_or_V[i-1][0], E_or_V[i][1]);
			return E_or_V[i-1][1] + dx * fxy.evaluate(E_or_V[i][0]-dx/2., ymid);
		}
		else{
			return E_or_V[i-1][1] + dx * fxy.evaluate(2*i - 1);
		}
	}
	
	public double getRK4(double[][] E_or_V, int i, double dx, Function fxy){
		if(fxy.getCharge()){
			double k1 = fxy.evaluate(E_or_V[i][0]-dx, E_or_V[i][1]);
			double k2 = fxy.evaluate(E_or_V[i][0]-dx/2., E_or_V[i][1]+dx*k1/2.);
			double k3 = fxy.evaluate(E_or_V[i][0]-dx/2., E_or_V[i][1]+dx*k2/2.);
			double k4 = fxy.evaluate(E_or_V[i][0], E_or_V[i][1]+dx*k3/2.);
			return E_or_V[i-1][1] + dx * (k1+2.*k2+2.*k3+k4)/6.;
		} else{
			double k1 = fxy.evaluate(2*(i-1));
			double k2 = fxy.evaluate(2*i - 1);
			double k3 = fxy.evaluate(2*i - 1);
			double k4 = fxy.evaluate(2*i);
			return E_or_V[i-1][1] + dx * (k1+2.*k2+2.*k3+k4)/6.;
		}
	}
	
	public double[][] getElectricField(){
		double[][] x_Ex = new double[n+1][4];
		Function chargeDensity = new Function();
		x_Ex[0][0] = x_min;
		x_Ex[0][1] = Ex0;
		x_Ex[0][2] = chargeDensity.evaluate(x_Ex[0][0], x_Ex[0][1]);
		if(order == 1){
			for(int i=1; i<=n; i++){
				x_Ex[i][0] = x_Ex[i-1][0] + dx;
				x_Ex[i][1] = this.getEuler(x_Ex, i, dx, chargeDensity);
				x_Ex[i][2] = chargeDensity.evaluate(x_Ex[i][0], x_Ex[i][1]);
				x_Ex[i][3] = Math.abs(Math.abs(x_Ex[i][1])-Math.abs(chargeDensity.getAnalytic(x_Ex[i][0], true)));
			}
		}else if(order == 2){
			for(int i=1; i<=n; i++){
				x_Ex[i][0] = x_Ex[i-1][0] + dx;
				x_Ex[i][1] = this.getRK2(x_Ex, i, dx, chargeDensity);
				//x_Ex[i][1] = this.getRK2(x_Ex[i-1][1], x_Ex[i][0], dx, chargeDensity);
				x_Ex[i][2] = chargeDensity.evaluate(x_Ex[i][0], x_Ex[i][1]);
				x_Ex[i][3] = Math.abs(Math.abs(x_Ex[i][1])-Math.abs(chargeDensity.getAnalytic(x_Ex[i][0], true)));
			}
		}else if(order == 4){
			for(int i=1; i<=n; i++){
				x_Ex[i][0] = x_Ex[i-1][0] + dx;
				x_Ex[i][1] = this.getRK4(x_Ex, i, dx, chargeDensity);
				//x_Ex[i][1] = this.getRK4(x_Ex[i-1][1], x_Ex[i][0], dx, chargeDensity);
				x_Ex[i][2] = chargeDensity.evaluate(x_Ex[i][0], x_Ex[i][1]);
				x_Ex[i][3] = Math.abs(Math.abs(x_Ex[i][1])-Math.abs(chargeDensity.getAnalytic(x_Ex[i][0], true)));
			}
		}
		return x_Ex;
	}
	
	public void writeElectricField(String outFile){
		MyFileWriter fw = new MyFileWriter();
		double[][] x_Ex = this.getElectricField();
		Matrix x_E_rho = new Matrix(x_Ex);
		fw.writeFile(outFile, x_E_rho);
	}
	
	public double[][] getElectricPotential(){
		double[][] x_Vx = new double[n+1][3];
		Function electricField = new Function(this.n, this.order);
		x_Vx[0][0] = x_min;
		x_Vx[0][1] = Vx0;
		if(order == 1){
			for(int i=1; i<=n; i++){
				x_Vx[i][0] = x_Vx[i-1][0] + dx;
				x_Vx[i][1] = this.getEuler(x_Vx, i, dx, electricField);
				x_Vx[i][2] = Math.abs(Math.abs(x_Vx[i][1])-Math.abs(electricField.getAnalytic(x_Vx[i][0], false)));
			}
		}else if(order == 2){
			for(int i=1; i<=n; i++){
				x_Vx[i][0] = x_Vx[i-1][0] + dx;
				x_Vx[i][1] = this.getRK2(x_Vx, i, dx, electricField);
				x_Vx[i][2] = Math.abs(Math.abs(x_Vx[i][1])-Math.abs(electricField.getAnalytic(x_Vx[i][0], false)));
			}
		}else if(order == 4){
			for(int i=1; i<=n; i++){
				x_Vx[i][0] = x_Vx[i-1][0] + dx;
				x_Vx[i][1] = this.getRK4(x_Vx, i, dx, electricField);
				x_Vx[i][2] = Math.abs(Math.abs(x_Vx[i][1])-Math.abs(electricField.getAnalytic(x_Vx[i][0], false)));
			}
		}
		return x_Vx;
	}
	
	public void writeElectricPotential(String outFile){
		MyFileWriter fw = new MyFileWriter();
		double[][] x_Vx = this.getElectricPotential();
		Matrix x_V = new Matrix(x_Vx);
		fw.writeFile(outFile, x_V);
	}
	
	public static void main(String[] args){
		System.out.println("HOLA");
		int n = 47;
		Efield Euler = new Efield(n, 1);
		Euler.writeElectricField("eulerEfield.dat");
		Euler.writeElectricPotential("eulerEpotential.dat");
		Efield RK2 = new Efield(n, 2);
		RK2.writeElectricField("rk2Efield.dat");
		RK2.writeElectricPotential("rk2Epotential.dat");
		Efield RK4 = new Efield(n, 4);
		RK4.writeElectricField("rk4Efield.dat");
		RK4.writeElectricPotential("rk4Epotential.dat");
	}

}
