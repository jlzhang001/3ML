import os, sys
import pkg_resources
import yaml

from threeML.config.config_checker import check_configuration


class Config( object ):
    
    def __init__( self ):
        
        # Read the config file
        
        # Define a list of possible path where the config file might be
        # The first successful path will be the active configuration file
        
        possiblePaths = []
        
        # First possible path is the .threeML directory under the user-home
        
        possiblePaths.append( os.path.join( os.path.expanduser( '~' ), '.threeML'  ) )
        
        # Second possible path is the config subdir under the package path
        # (which is where this config.py file is)

        distribution = pkg_resources.get_distribution("threeML")
        distribution_path = os.path.join(distribution.location, 'threeML/config')

        # possiblePaths.append( os.path.join( distribution.location, 'threeML/config' ) )

        self._configuration = None
        self._filename = None
        
        for path in possiblePaths:
            
            thisFilename = os.path.join( path, 'threeML_config.yml' )
            
            if os.path.exists( thisFilename ):
                
                with open( thisFilename ) as f:

                    configuration = yaml.safe_load(f)

                    # Test if the local/configuration is ok

                    if check_configuration(configuration, f):

                        self._configuration = configuration

                        print("Configuration read from %s" % (thisFilename))



                

                
                self._filename = thisFilename
                
                break
            
            else:
                
                continue
        
        if self._configuration is None:

            # First we will try to load the default configuration

            thisFilename = os.path.join(distribution_path, 'threeML_config.yml')

            if os.path.exists(thisFilename):

                with open(thisFilename) as f:

                    configuration = yaml.safe_load(f)

                    # Test if the distribution configuration

                    if check_configuration(configuration, f):

                        self._configuration = configuration

                        print("Default configuration read from %s" % (thisFilename))

                    else:

                        possiblePaths.append(distribution_path)

                        print('Default configuration is corrupted')

        if self._configuration is None:

            
            raise RuntimeError("Could not find threeML_config.yml in any of %s" %( possiblePaths ))

    
    def __getitem__(self, key):
        
        if key in self._configuration.keys():
            
            return self._configuration[ key ]
        
        else:
            
            raise RuntimeError("Configuration key %s does not exist in %s." %( key, self._filename ) )
    
    def __repr__(self):
        
        return yaml.dump( self._configuration, default_flow_style=False )

    def restore_default_configuration(self):
        """
        Restore the default configuration

        :return:

        """

        distribution = pkg_resources.get_distribution("threeML")
        distribution_path = os.path.join(distribution.location, 'threeML/config')

        thisFilename = os.path.join(distribution_path, 'threeML_config.yml')

        if os.path.exists(thisFilename):

            with open(thisFilename) as f:

                configuration = yaml.safe_load(f)

                # Test if the distribution configuration

                if check_configuration(configuration, f):

                    self._configuration = configuration

                    print("Default configuration read from %s" % (thisFilename))

                else:

                    print('Default configuration is corrupted')

    def restore_user_configuration(self):
        """
        Restore the user configuration if it exists.


        :return:
        """

        self.__init__()



# Now read the config file, so it will be available as Config.c
threeML_config = Config()

