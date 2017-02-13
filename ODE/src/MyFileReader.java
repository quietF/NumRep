//
//  MyFileReader.java
//  
//  A minimal I/O package to read data from a text file.
//  The text file needs to be a set of (any number of) columns separated by whitespace, eg:
//
//  1.0  0.1 
//  2.0  0.2
//  3.0  0.3
//
//  It is presented to the user in the form of a nxm matrix where 
//    n = number of rows = number of line in file 
//    m = number of columns = number of entries on each line
//
//  The user can also ask for individual columns.
//
//  For use in Numerical Recipes course.
//
//  Created by PeterClarke on 30/07/2013.
//

import java.util.*;
import java.io.*;
import Jama.*;



public class MyFileReader {
	
	private String filename ;
	private Matrix M ;
	boolean isValid = false ;
	
	//.......................
	// Constructor
	public MyFileReader ( String _filename ) {

		filename = _filename ;
			
		List<Double> list = new ArrayList<Double>();
		File file = new File(filename);
		BufferedReader reader = null;
	
		int nrows=0;
		int ncols=0;
		
		try {
			reader = new BufferedReader(new FileReader(file));
			String text = null;
		
			while ((text = reader.readLine()) != null) {
				
				nrows++;
				String[] tokens = text.split("\\s+") ;
				ncols = tokens.length;
				
				for( int ind=0; ind < tokens.length; ++ind) {
					list.add(Double.parseDouble(tokens[ind]));
				}
				
			}
			
			M = new Matrix( nrows, ncols ) ;
			isValid = true ;
			
			for( int irow=0; irow<nrows; ++irow ) {
				for( int icol=0; icol< ncols; ++icol ) {
					int ind = irow*ncols+icol ;
					M.set(irow,icol,list.get(ind)) ;
				}
			}

			//print out the list
			//System.out.println(list);
			//M.print(5,3) ;
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (reader != null) {
					reader.close();
				}
			} catch (IOException e) {
			}
		}
	}
	
	//..............
	// is it valid
	public boolean isValid() {
		return isValid ;
	}
	
	//..............
	// Get number of rows
	public int getRowDimension() {
		return M.getRowDimension();
	}

	//..............
	// Get number of columns
	public int getColumnDimension() {
		return M.getColumnDimension();
	}
	
	//..............
	//Get the whole matrix
	public Matrix getMatrix() {
		return M ;
	}

	//..............
	//Get a column
	public Matrix getColumn( int icol ) {
		if( (icol>=0) && (icol < M.getColumnDimension()) ) {
			return M.getMatrix( 0, M.getRowDimension()-1, icol, icol ) ;
		}
		else {
			return null ;
		}
	}
	
	//...............
	// Print out data set
	public void print() {
		if( isValid ) {
			String msg = "Dataset rows= "+Integer.toString(M.getRowDimension())+" / colums = "+Integer.toString(M.getColumnDimension());
			System.out.println(msg);
			M.print(5,3) ;
		}
		else
			System.out.println("Data set is not valid");
	}

			
	
}

