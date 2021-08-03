import gdb
import argparse

class ShowNodes(gdb.Command):
    """Show info about node object"""

    def __init__(self):
        super(ShowNodes, self).__init__("show-nodes", gdb.COMMAND_USER)
    
    def get_parser(self):
        parser = argparse.ArgumentParser(description=ShowNodes.__doc__)
        parser.add_argument("-a", "--addr", help="Address of the node")
        parser.add_argument("-v", "--varname", help="Name of the variable")
        parser.add_argument("-i", "--index", help="Index of the variable from gdb history")
        return parser

    def get_obj_from_addr(self, objtype, addr):
        gdbval = gdb.Value(int(addr, 16))
        return gdbval.cast(gdb.lookup_type(objtype).pointer())
    
    def get_obj_from_var(self, var):
        return gdb.parse_and_eval(var)
    
    def get_obj_from_history(self, index):
        # gdb.history() takes negative index too, similar to lists.
        # (-1) will return the last element in the current history
        # raises gdb.error if the history hasn't reached the given index
        return gdb.history(index)
    
    def parse_args(self, args):
        try:
            parser = self.get_parser()
            parsed_args = parser.parse_args(args)
            return parsed_args
        except(SystemExit):
            # parse_args throws SystemExit when the args are 
            # invalid or help is needed.
            return None

    def invoke(self, argument, from_tty):
        # gdb.string_to_argv converts argument into sys.argv style
        argv = gdb.string_to_argv(argument)
        args = self.parse_args(argv)

        if not args:
            # parsing failed. return early.
            return

        if args.addr:
            self.print_node(self.get_obj_from_addr("node_t", args.addr))
        if args.varname:
            self.print_node(self.get_obj_from_var(args.varname))
        if args.index:
            node = self.get_obj_from_history(int(args.index))
            node_ptr = gdb.lookup_type("node_t").pointer()
            if node and (node.type == node_ptr):
                self.print_node(node)
            else:
                print("No {} object found at index {}".format("struct node *", args.index))

    def print_node(self, node):
        print("id={}, name={}, timestamp={}".format(node["id"], node["name"].string(), node["creation_time"]))

ShowNodes()