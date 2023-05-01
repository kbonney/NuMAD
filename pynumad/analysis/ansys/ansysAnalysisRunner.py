from pynumad.analysis.ansys.read import *
from pynumad.analysis.ansys.write import writeAnsysShellModel

class ansysAnalysisRunner():
    """
    """

    def __init__(self, blade, meshData: dict, loads: list, config: dict):
        self.config = config
        self.blade = blade

    
    def writeShellModel(self, filename, meshData, config):
        writeAnsysShellModel(self.blade, filename, meshData, config)

    
    def writeAnalysisScript(self):
        ## ************************************************************************
        # ================= APPLY LOADS TO FEA MESH ================= #NOTE: Priority
        forcefilename = 'forces'
        nodeData = np.concatenate([np.arange(meshData['nodes'].shape[0]).reshape((-1,1)),meshData['nodes']], axis=1)
        loads = loadsTable[iLoad]
        write_ansys_loads(nodeData, loads, forcefilename, analysisConfig)

        ## ************************************************************************
        # ================= PERFORM LINEAR STATIC ANALYSIS ================= #NOTE: Priority
        # run buckling computations in ansys
        print(' ')
        print('Running ANSYS analysis...')
        script_name = 'ansysAnalysis.mac'
        script_out = 'ansysAnalysisEcho.out'
        fid = open(script_name,'w+')
        fid.write('/NERR,,99999999\n' % ())
        fid.write('/CWD, %s\n' % (os.getcwd()))
        fid.write('resume,master,db\n' % ())
        #         fprintf(fid,'/FILNAME,''#s'',1\n',ansysFilename);   #From master, change the jobname
        fid.write('/FILNAME,%s,1\n' % (ansysFilename+'-Load'+str(iLoad)))
        #fprintf(fid,'resume\n');
        fid.write('! BEGIN LINEAR STATIC SCRIPT\n' % ())
        fid.write('esel,all\n' % ())
        fid.write('/prep7\n' % ())
        fid.write('fdel,all\n' % ())
        fid.write('/input,%s,src\n' % (forcefilename))
        #Linear Static Analysis
        fid.write('/solu\n' % ())
        fid.write('antype,static\n' % ())
        if 'StaticNonlinear' in analysisConfig["analysisFlags"] and not \
            len(analysisConfig["analysisFlags"].StaticNonlinear)==0  and \
            analysisConfig["analysisFlags"].StaticNonlinear != 0:
            fid.write('nlgeom,1\n' % ())
            fid.write('OUTRES,all,ALL\n' % ())
        #         else
        #             fprintf(fid,'pstres,on\n');
        fid.write('irlf,-1\n' % ())
        fid.write('bcsoption,,incore\n' % ())
        fid.write('solve\n' % ())
        fid.write('finish\n' % ())
        #Only compute mass on the first load case
        if iLoad == 0 and 'mass' in analysisConfig["analysisFlags"] and \
            analysisConfig["analysisFlags"]['mass'] != 0:
            #Get Mass Here
            fid.write('*GET, Z_mass, ELEM, 0, MTOT, X\n' % ())
            fid.write('/output, mass,txt\n' % ())
            fid.write('*status,Z_mass\n' % ())
            fid.write('/output\n' % ())
            fid.write('finish\n' % ())
        ## ************************************************************************
        #================= PERFORM Deflection ANALYSIS =================  #NOTE: Priority
        if 'deflection' in analysisConfig["analysisFlags"] and \
            analysisConfig["analysisFlags"]['deflection'] != 0:
            deflectionFilename = 'results_deflection'
            writeAnsysDeflections(blade,analysisConfig,iLoad,fid,deflectionFilename)
        # calculate face stresses for wrinkling NOTE: Skip
        if 'localBuckling' in analysisConfig["analysisFlags"] and not \
                'imperfection' in analysisConfig["analysisFlags"] and not \
                 len(analysisConfig["analysisFlags"].imperfection)==0:
            #Check for wrinkling here in a linear analysis
            app,SkinAreas,compsInModel = writeAnsysGetFaceStresses(blade,fid,analysisConfig["analysisFlags"].localBuckling)
        ### Output resultant force and moments to file NOTE: Skip
        if 'resultantVSspan' in analysisConfig["analysisFlags"] and \
            analysisConfig["analysisFlags"].resultantVSspan != 0:
            writeAnsysResultantVSSpan(blade,analysisConfig,iLoad,fid)
        ## ************************************************************************
        # ================= PERFORM FATIGUE ANALYSIS ================= 
        if 'fatigue' in analysisConfig["analysisFlags"]:
            writeAnsysFatigue(fid,iLoad)
        ## ************************************************************************
        # ================= CREAT LOCAL FIELD RESULTS FOR MATLAB ================= #NOTE: Priority
        if 'localFields' in analysisConfig["analysisFlags"]:
            writeAnsysLocalFields(blade,analysisConfig,iLoad,fid)
        ## ************************************************************************
        # ================= PERFORM FAILURE ANALYSIS ================= #NOTE: Priority
        # Initialize GUI commands from batch operation to identify maxima
        if 'failure' in analysisConfig["analysisFlags"]:
            failureFilename = 'results_failure'
            writeAnsysRupture(analysisConfig,iLoad,fid,failureFilename)
        ## ************************************************************************
        # ================= PERFORM BUCKLING ANALYSIS ================= #NOTE: Priority
        #Linear Buckling Analysis
        if 'globalBuckling' in analysisConfig["analysisFlags"] and \
            analysisConfig["analysisFlags"]['globalBuckling'] > 0:
            bucklingFilename = 'results_buckling'
            writeAnsysLinearBuckling(blade,analysisConfig,iLoad,fid,bucklingFilename)
        else:
            if 'globalBuckling' in analysisConfig["analysisFlags"] and analysisConfig["analysisFlags"]['globalBuckling'] < 0:
                raise Exception('analysisConfig["analysisFlags"].globalBuckling must be greater than or equal to zero')
        fid.close()

        ## ************************************************************************
        # ================= SEND COMMANDS TO ANSYS =================
        args = (ansysPath,ansys_product,script_name,script_out,str(ncpus))
        ansys_call = 'export KMP_STACKSIZE=2048k & %s -b -p %s -I %s -o %s -np %s' % args
        #         KMP_STACKSIZE is 512k by default. This is not enough therefore SET
        #         KMP_STACKSIZE=2048k has been specifed. 2048k may not be enough for other
        #         simulations. EC
        ansys_ps = subprocess.run(ansys_call, shell=True)      

        #  MATLAB POST PROCESS ##########################################
        ## ************************************************************************
        # ================= READ MASS RESULTS INTO MATLAB =================
        if iLoad == 0 and 'mass' in analysisConfig["analysisFlags"] and \
            analysisConfig["analysisFlags"]['mass'] != 0:
            designvar.mass = read_1_ANSYSoutput('mass.txt')
            # delete mass.txt
        ## ************************************************************************
        # ================= READ DEFLECTION RESULTS INTO MATLAB =================
        if 'deflection' in analysisConfig["analysisFlags"] and analysisConfig["analysisFlags"]['deflection'] != 0:
            designvar['deflection'] = readAnsysDeflections(blade,analysisConfig,iLoad,deflectionFilename)
        ## ************************************************************************
        # ================= READ STRESS RESULTANTS INTO MATLAB =================
        if 'resultantVSspan' in analysisConfig["analysisFlags"] and analysisConfig["analysisFlags"]['resultantVSspan'] != 0:
            fileName = 'resultantVSspan.txt'
            designvar.resultantVSspan[iLoad] = txt2mat(fileName)
            os.delete(fileName)
            #             fileName='resultantVSspan2.txt';
            #             designvar.resultantVSspan2{iLoad}=txt2mat(fileName);
            #             delete(fileName);
        ## ************************************************************************
        # ================= READ LINEAR BUCKLING RESULTS =================
        # read buckling results
        if 'globalBuckling' in analysisConfig["analysisFlags"] and analysisConfig["analysisFlags"]['globalBuckling'] > 0:
            linearLoadFactors = readAnsysLinearBuckling(blade,analysisConfig,iLoad,fid,bucklingFilename)
        ## ************************************************************************
        # ================= PERFORM NON-LINEAR BUCKLING/WRINKLING ANALYSIS =================
        # Perform nonlinear buckling here if required (and writeANSYSgetFaceStresses
        # at the end of the nonlinear analysis for wrikling check
        if 'imperfection' in analysisConfig["analysisFlags"] and not len(analysisConfig["analysisFlags"]['imperfection'])==0 :
            warnings.warn('output designvar. Currently does not work for nonlinear cases')
            imperfection = analysisConfig["analysisFlags"].imperfection / 1000
            nonlinearLoadFactors = np.zeros((len(linearLoadFactors),len(imperfection)))
            critDesignvar = np.zeros((len(imperfection),1))
            wrinklingLimitingElementData = np.zeros((len(linearLoadFactors),4,len(imperfection)))
            marker = np.array(['-ok','-sk','-dk','-*k','-^k','-<k','->k','-pk','-hk'])
            #SF=max(LLF); #Use one loads file for all buckling modes
            for jj in range(len(imperfection)):
                for ii in range(len(linearLoadFactors)):
                    # For each load factor, create a new jobname and database and run a nonlinear static analysis
                    nonlinearLoadFactors[ii,jj] = writeAnsysNonLinearBuckling(ansysFilename,ansysPath,ansys_product,analysisConfig,ii,jj,ncpus,iLoad)
                    wrinklingLimitingElementData[ii,:,jj] = wrinklingForNonlinearBuckling(blade,analysisConfig["analysisFlags"].localBuckling,settings,ncpus,ansysFilename,ii,jj)
                minnLLF,minnLLFMode = np.amin(nonlinearLoadFactors[:,jj])
                minWLF,minWLFMode = np.amin(wrinklingLimitingElementData[:,2,jj])
                critDesignvar[jj] = np.amin(minnLLF,minWLF)
            plt.figure(5)
            for k in range(len(linearLoadFactors)):
                #disp(strcat('-',marker(j),'k'))
                plt.plot(imperfection * 1000,nonlinearLoadFactors[k,:],marker[k])
                hold('on')
            plt.legend('Mode-' + str(np.arange(len(linearLoadFactors))))
            plt.title('Imperfection Study (Linear Elements) SNL3p0-148-mk0p2-s1-fiberglass')
            plt.xlabel('Max Imperfection Size [mm]')
            plt.ylabel('Buckling Load Factors [ ]')
            #wrinklingLimitingElementData - [ansysSecNumber elno lf phicr]
            designvar.globalBuckling[iLoad] = np.amin(np.amin(critDesignvar))
        else:
            if 'globalBuckling' in analysisConfig["analysisFlags"] and analysisConfig["analysisFlags"].globalBuckling > 0:
                designvar.globalBuckling[iLoad] = linearLoadFactors(1)
        ## ************************************************************************
        # ================= POST-PROCESS PANEL WRINKLING FACTORS =================
        if 'localBuckling' in analysisConfig["analysisFlags"] and not \
            len(analysisConfig["analysisFlags"].localBuckling)==0:
            if 'imperfection' in analysisConfig["analysisFlags"] and not \
                len(analysisConfig["analysisFlags"].imperfection)==0 :
                #UNSUPPORTED AT THIS TIME
                writeAnsysNonLinearLocalBuckling(blade,analysisConfig,iLoad,fid,ansysFilename,ii,jj)
            # perform wrinkling check
            wrinklingLimitingElementData = writeAnsysFagerberWrinkling(app,SkinAreas,compsInModel,analysisConfig["analysisFlags"].localBuckling)
            designvar.localBuckling[iLoad] = wrinklingLimitingElementData[2]
            os.path.delete('*faceAvgStresses.txt') # NOTE: I believe * is supposed to glob here, but I am not sure it is doing that -kb
        