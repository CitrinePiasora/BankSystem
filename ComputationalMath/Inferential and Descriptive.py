import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statistics

df = pd.read_csv(r"C:\Users\Djagad P. Dwialam\Desktop\Compmath Project\Height vs Shoe Size.csv") # change this later
df.fillna(0, inplace = True)

while(True):
    print("\nWhich topic would you like to try out?\n1. Descriptive Statistics\n2. Inferential Statistics\n3. Exit")

    choice = eval(input(">>> "))

    if choice == 1:
        print("\nThe Dataset used is Data of Measured Heights and Foot Size:\n1. Mean\Mode\Median\n2. Standard Deviation\Variance\n3. Scatter Plot\n4. Normal Distribution\n5. Skew\n6. Kurtosis")

        choice = eval(input(">>> "))

        if choice == 1:
            
            a = np.array(df['height'])
            b = np.array(df['foot size'])

            meanHeight, meanSize = np.mean(a), np.mean(b)
            modeHeight, HeightFreq, modeSize, SizeFreq = float(stats.mode(a)[0]), float(stats.mode(a)[1]), float(stats.mode(b)[0]), float(stats.mode(b)[1]) 
            medianHeight, medianSize = np.median(a), np.median(b)

            print("Below is the summary for the Dataset")
            print("\nMean:\nHeight: %.2f Inches\nFoot Size: %.2f Inches" % (meanHeight, meanSize))

            print("\nMode:\nHeight, Freq: %.2f Inches, %d times\nFoot Size, Freq: %.2f Inches, %d times" % (modeHeight, HeightFreq, modeSize, SizeFreq))

            print("\nMedian:\nHeight: %.2f Inches\nFoot Size: %.2f Inches" % (medianHeight, medianSize))

        elif choice == 2:

            a = np.array(df['height'])
            b = np.array(df['foot size'])

            stdHeight, stdSize = np.std(a), np.std(b)
            varHeight, varSize = statistics.variance(a), statistics.variance(b)

            print("\nStandard Deviation:\nHeight: %.2f Inches\nFoot Size: %.2f Inches" % (stdHeight, stdSize))

            print("\nVariance:\nHeight: %.2f Inches\nFoot Size: %.2f Inches" % (varHeight, varSize))

        elif choice == 3:

            df.plot.scatter(x = 'foot size', y = 'height')
            plt.show()

        elif choice == 4:

            fig, axes = plt.subplots(nrows=2)
            fig.set_size_inches(15, 15)

            a = np.array(df['height'])
            b = np.array(df['foot size'])
            
            aNorm = stats.norm(loc = np.mean(a), scale = np.std(a))
            bNorm = stats.norm(loc = np.mean(b), scale = np.std(b))

            aSamples = aNorm.rvs(500)
            bSamples = bNorm.rvs(500)

            axes[0].hist(aSamples, density=1, bins=30, edgecolor="cyan", linewidth=0.5, color="magenta")
            axes[0].plot(np.linspace(50, 85), aNorm.pdf(np.linspace(50, 85)), color="yellow", linewidth=5)
            
            axes[1].hist(bSamples, density=1, bins=30, edgecolor="cyan", linewidth=0.5, color="magenta")
            axes[1].plot(np.linspace(3, 15), bNorm.pdf(np.linspace(3, 15)), color="yellow", linewidth=5)

            plt.show()

        elif choice == 5:
            a = np.array(df['height'])
            b = np.array(df['foot size'])

            skewHeight, skewSize = stats.skew(a), stats.skew(b)

            print("\nSkew Height: %f\nSkew Foot Size: %f" % (skewHeight, skewSize))

        elif choice == 6:
            fig, axes = plt.subplots(nrows=2)
            fig.set_size_inches(15, 15)

            a = np.array(df['height'])
            b = np.array(df['foot size'])

            stats.kurtosis(a)
            stats.kurtosis(b)

            axes[0].hist(a)
            axes[0].set_title("Height")

            axes[1].hist(b)
            axes[0].set_title("Foot Size")

            plt.show()

    elif choice == 2:
        print("\nThe Dataset used is Data of Measured Heights and Foot Size:\n1. Pearson's Correlation\n2. Z-Scores\n3. Normal Distribution using Z-Score\n4. Hypothesis Testing with T-test")

        choice = eval(input(">>> "))

        if choice == 1:
            a = np.array(df['height'])
            b = np.array(df['foot size'])

            r = np.corrcoef(a, b) 

            print("The Correlation between Height and Foot Size is: \n" , r)

            plt.scatter(a, b)
            plt.ylabel("Foot Size")
            plt.xlabel("Height")
            plt.show()
        
        elif choice == 2:
            a = np.array(df['height'])
            b = np.array(df['foot size'])
            print("\n Z-Score for the first array is : \n", stats.zscore(a))
            print("\n Z-Score for the second array is : \n", stats.zscore(b))
            
            fig, axes = plt.subplots(nrows=4)
            fig.set_size_inches(15, 15)

            axes[0].hist(a)
            axes[0].set_title("Height")
            
            axes[2].hist(stats.zscore(a))
            axes[2].set_title("Height Z-Score")

            axes[1].hist(b)
            axes[1].set_title("Foot Size")

            axes[3].hist(stats.zscore(b))
            axes[3].set_title("Foot Size Z-Score")

            plt.show()

        elif choice == 3:
            
            fig, axes = plt.subplots(nrows=2)
            fig.set_size_inches(15, 15)

            a = np.array(df['height'])
            b = np.array(df['foot size'])
            print("\n Z-Score for Height: \n", stats.zscore(a))
            print("\n Z-Score for Foot Size: \n", stats.zscore(b))

            axes[0].hist(stats.zscore(a))
            axes[1].hist(stats.zscore(b))

            plt.show()

            
            
        elif choice == 4:
            a = np.array(df['height'])
            b = np.array(df['foot size'])

            print("Height mean is: %f\nFoot size mean is: %f\n" % (np.mean(a), np.mean(b)))

            print("Height std vale is: %f\nFoot size std value is: %f\n" % (np.std(a), np.std(b)))

            ttest,pval = stats.ttest_ind(a,b)
            print("p-value =", pval)

            if pval < 0.05:
                print("Reject Null hypothesis")
            else:
                print("Accept Null hypothesis")
    
    elif choice == 3:
        break
