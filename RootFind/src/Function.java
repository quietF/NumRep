
public class Function {

	char function;
	public Function(char function) throws Exception{
		if(function=='f' || function=='g' || function=='h')
			this.function = function;
		else throw new Exception("char must be 'f', 'g', or 'h'.");
	}
	/*
	 * class for evaluation of functions:
	 * i) f(x) = 10.2 - 7.4x - 2.1x^2 + x^3
	 * ii) g(x) = e^x - 2
	 * iii) h(x) = cos(x)sin(3x)
	 */
	
	public double evaluate(double x){
		if(function=='f')
			return 10.2 - 7.4*x - 2.1*x*x + x*x*x;
		else if(function=='g')
			return Math.exp(x) - 2.;
		else if(function=='h')
			return Math.cos(x)*Math.sin(3.*x);
		else{
			System.out.println("Error - 'f', 'g', or 'h'.");
			return 0.;
		}
	}

}
