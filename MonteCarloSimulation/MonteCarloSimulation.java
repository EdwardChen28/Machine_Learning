import java.util.*;
import java.util.HashMap;
import java.lang.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Flexible_MonteCarloSimulationP4P5{
	private static int[][] parents;
	private static double[][] cpt;

	public static void initialization(){
		int nNode = 0;
		// read file. need to specify the path of the file
		String filename = "network2.txt";
		//String filename = "network1.txt";
		try{
			FileReader filereader = new FileReader(filename);
			BufferedReader bufferReader = new BufferedReader(filereader);
			String line = null;
			//get the number of nodes we have
			if((line = bufferReader.readLine()) != null) nNode = Integer.parseInt(line);
			parents = new int[nNode][]; 
			cpt = new double[nNode][];
			int count = 0;
			//read parents 
			while((line = bufferReader.readLine()) != null){
				String[] splited = line.split(" ");
				int id = Integer.parseInt(splited[0]);
				if(count < nNode){
					int nParents = Integer.parseInt(splited[1]);
					parents[id] = new int[nParents];
					for(int i = 2; i < splited.length; i++){
						parents[id][i-2] = Integer.parseInt(splited[i]);
					}
				}
				else{
					int len = splited.length-1;
					cpt[id] = new double[len]; 
					for(int i = 1; i < splited.length; i++){
						cpt[id][i-1] = Double.parseDouble(splited[i]);
					}
				}
				count++;
			}
		}catch(IOException e){
			e.printStackTrace();
		}// end of try
	}


	public static void run(int[][] parents, double[][] cpt, int n){
		Random rand = new Random();
		int len = parents.length;
		double guess, mean, std;
		int index;
		boolean[] binary = new boolean[len];
		double[] satisfied = new double[10];
		for(int t = 0; t < 10; t++){
			int count = 0;
			for(int k = 0; k < n; k++){
				for(int i = 0 ; i < len; i++){
					// check if it has parent/s or not
					index = getIndex(parents[i], binary);
					guess = rand.nextDouble();
					if(guess <= cpt[i][index]) binary[i] = true;
					else binary[i] = false;
				}
				//**********************Problem 5 Test ********************
				// check condition Network2
				// if condition satisfied, count. otherwise, reject sample
				if(binary[0]==true && binary[3] == false && binary[2] == true)
					count++;

				//***********************Problem 4 Test*********************
				// check condition network1. a)
				// if(binary[0] && !binary[1] && binary[2] && !binary[3] && binary[4] &&binary[5]&& !binary[6])
				// 	count++;

				// check condition network1. b)
				//if(!binary[6] && binary[4]) count++;

				// check condition network1. c)
				//if(!binary[0] && binary[1] && binary[5]) count++;
			}
			satisfied[t] = (double)count/n;
		}

		//find mean
	 	double sum = 0.0;
	 	for(int i = 0; i < 10; i++) sum+=satisfied[i];
	 	mean = sum/10;
	 	mean = (double) Math.round(mean*1000d)/1000d;
	 	sum = 0.0;
	 	for(int i = 0; i< 10; i++) sum += Math.pow(mean-satisfied[i], 2);
	 	std = Math.sqrt(sum/10);
	 	std = (double) Math.round(std*1000d)/1000d;

	 	//******************** print output **************
	 	//Network2
	 	System.out.println("P(C=T | A=T, D=F) running "+n+" times, mean: "+mean+", std: "+std);
	
	 	// Network1, a)
	 	//System.out.println("P(A=T, B=F,C=T, D=F,E=T,F=T,G=F) running "+n+" times, mean: "+mean+", std: "+std);

	 	// network1, b)
	 	//System.out.println("P(E=T | G=F) running "+n+" times, mean: "+mean+", std: "+std);

	 	//network1, c)
	 	//System.out.println("P(F=T | A=F, B=T) running "+n+" times, mean: "+mean+", std: "+std);
	}

	public static int getIndex(int[] parents, boolean[] binary){
		if(parents.length == 0) return 0;
		int numberOfParents = parents.length;
		int sum = 0;
		if(numberOfParents == 1) return binary[parents[0]] ==true? 0: 1;
		if(numberOfParents == 2){
			if(binary[parents[0]] == true) sum+=0;
			else sum+=2;
			if(binary[parents[1]] == true) sum+=0;
			else sum+=1;
		}

		return sum;
	}

	public static void printData(int[][] parents, double[][] cpt){
		for(int i = 0; i < parents.length; i++){
			System.out.print(i);
			for(int j = 0 ; j < parents[i].length; j++){
				System.out.print(" "+parents[i][j]);
			}
			System.out.println();
		}

		for(int i = 0; i < cpt.length; i++){
			System.out.print(i);
			for(int j = 0 ; j < cpt[i].length; j++){
				System.out.print(" "+cpt[i][j]);
			}
			System.out.println();
		}

	}

	public static void main(String[] args){
		initialization();
		run(parents,cpt,100);
		run(parents,cpt,1000);
		run(parents,cpt,10000);
		run(parents,cpt,100000);
	}





}