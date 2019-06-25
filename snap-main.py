# Import the interface required by the Script snap.
from com.snaplogic.scripting.language import ScriptHook
import java.util
import json
import collections


def dig_logs(in_rec, errors=[], path=None):
    
    if type(in_rec) is dict:
        for key, val in in_rec.items():
            # path = path + '.' + key if path else key
            if key == 'reason':
                # errors.append({'path': path, 'error' : val})
                errors.append(val)
            elif type(val) is dict or list:
                path = path + '.' + key if path else key    
                dig_logs(val, errors, path)
    elif type(in_rec) is list:
        [dig_logs(x, errors, path) for x in in_rec]
    return errors

class TransformScript(ScriptHook):
    def __init__(self, input, output, error, log):
        self.input = input
        self.output = output
        self.error = error
        self.log = log

    # The "execute()" method is called once when the pipeline is started
    # and allowed to process its inputs or just send data to its outputs.
    def execute(self):
        self.log.info("Executing Transform script")
        while self.input.hasNext():
            try:
                # Read the next document, wrap it in a map and write out the wrapper
                in_doc = self.input.next()
                in_rec = json.loads(in_doc['doc'])
                errors = dig_logs(in_rec)
                summary = collections.Counter(errors)
                out_doc = java.util.HashMap()
                out_doc['summary'] = summary

                self.output.write(out_doc)
            except Exception as e:
                errWrapper = {
                    'errMsg' : str(e.args)
                }
                self.log.error("Error in python script")
                self.error.write(errWrapper)

        self.log.info("Finished executing the Transform script")

# The Script Snap will look for a ScriptHook object in the "hook"
# variable.  The snap will then call the hook's "execute" method.
hook = TransformScript(input, output, error, log)