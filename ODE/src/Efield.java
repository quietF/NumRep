import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;

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
	private double dx = (x_max-x_min)/(double)n;

	
	
	public Efield(int n, int order) throws FileNotFoundException, UnsupportedEncodingException {
		this.n = n;
		dx = (x_max-x_min)/(double)n;
	}

	public double getChargeDensity(double x, double y){
		if(x >= x_min){
			if(x < 1 || x >=3) return 0.;
			else if(x >= 1 && x < 2) return 1.;
			else return -1.;
		} else{
			System.out.println(x + ": Only possitive input values <= 4.");
		}
		return 3.;
	}
	
	public double getEuler(double ybefore, double xnow, double dx, Function fxy){
		return ybefore + dx * fxy.evaluateChargeDensity(xnow-dx, ybefore);
	}
	
	public double getRK2(double ybefore, double xnow, double dx, Function fxy){
		double ymid = ybefore + dx * fxy.evaluateChargeDensity(xnow-dx, ybefore);
		return ybefore + dx * fxy.evaluateChargeDensity(xnow-dx/2, ymid);
	}
	
	public double getRK4(double ybefore,double xnow, double dx, Function fxy){
		double k1 = fxy.evaluateChargeDensity(xnow - dx, ybefore);
		double k2 = fxy.evaluateChargeDensity(xnow - dx/2, ybefore + dx*k1/2.);
		double k3 = fxy.evaluateChargeDensity(xnow - dx/2, ybefore + dx*k2/2.);
		double k4 = fxy.evaluateChargeDensity(xnow, ybefore + dx*k3/2.);
		return ybefore + dx * (k1 + 2. * k2 + 2. * k3 + k4)/(double)6;
	}
	
	public double[][] getElectricField(int order, String outFile) throws FileNotFoundException, UnsupportedEncodingException{
		PrintWriter writer;
		writer = new PrintWriter(outFile, "UTF-8");
		MyFileWriter fw = new MyFileWriter();
		double[][] x_Ex = new double[n+1][3];
		Function chargeDensity = new Function();
		x_Ex[0][0] = x_min;
		x_Ex[0][1] = Ex0;
		x_Ex[0][2] = chargeDensity.evaluateChargeDensity(x_Ex[0][0], x_Ex[0][1]);
		if(order == 1){
			for(int i=1; i<=n; i++){
				x_Ex[i][0] = x_Ex[i-1][0] + dx;
				x_Ex[i][1] = this.getEuler(x_Ex[i-1][1], x_Ex[i][0], dx, chargeDensity);
				x_Ex[i][2] = chargeDensity.evaluateChargeDensity(x_Ex[i][1], x_Ex[i][1]);
				writer.println(x_Ex[i][0] + " " + x_Ex[i][1] + " " + chargeDensity.evaluateChargeDensity(x_Ex[i][0], x_Ex[i][1]));
			}
		}else if(order == 2){
			for(int i=1; i<=n; i++){
				x_Ex[i][0] = x_Ex[i-1][0] + dx;
				x_Ex[i][1] = this.getRK2(x_Ex[i-1][1], x_Ex[i][0], dx, chargeDensity);
				x_Ex[i][2] = chargeDensity.evaluateChargeDensity(x_Ex[i][1], x_Ex[i][1]);
				writer.println(x_Ex[i][0] + " " + x_Ex[i][1] + " " + chargeDensity.evaluateChargeDensity(x_Ex[i][0], x_Ex[i][1]));
			}
		}else if(order == 4){
			for(int i=1; i<=n; i++){
				x_Ex[i][0] = x_Ex[i-1][0] + dx;
				x_Ex[i][1] = this.getRK4(x_Ex[i-1][1], x_Ex[i][0], dx, chargeDensity);
				x_Ex[i][2] = chargeDensity.evaluateChargeDensity(x_Ex[i][1], x_Ex[i][1]);
				writer.println(x_Ex[i][0] + " " + x_Ex[i][1] + " " + chargeDensity.evaluateChargeDensity(x_Ex[i][0], x_Ex[i][1]));
			}
		}
		writer.close();
		return x_Ex;
	}
	
	public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException {
		System.out.println("HOLA");
		Efield Euler = new Efield(16, 1);
		Euler.getElectricField(1, "eulerEfield.dat");
		Efield RK2 = new Efield(16, 2);
		RK2.getElectricField(2, "rk2Efield.dat");
		Efield RK4 = new Efield(16, 4);
		RK4.getElectricField(4, "rk4Efield.dat");
	}

}
