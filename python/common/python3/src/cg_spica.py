#!/usr/bin/env python

import sys, textwrap
from pathlib import Path
sys.path.append(Path(__file__).parents[0].resolve())
import gen_top_ENM, json_to_top, map_to_cg, map_traj
from argparse import ArgumentParser, RawTextHelpFormatter

def get_option():
    argparser = ArgumentParser(add_help=False, formatter_class=RawTextHelpFormatter,
                               usage=textwrap.dedent("""\
                                      cg_spica tool_name 

                                      # list of tool_names #------------------------------------------------
                                      json2top : make top file from json file  
                                      map2cg   : map AA configuration to CG (only PDB format).  
                                      maptraj  : map AA MD trajectory to CG (MDAnalysis module is required).  
                                      ENM      : generate top file of protein with elastic network.
                                      ----------------------------------------------------------------------
                                                 """))
    argparser.add_argument('tool_name', type=str,
                            help='input tool_name.')
    return argparser

if __name__ == "__main__":
    ap        = get_option()
    args, sub = ap.parse_known_args()
    if args.tool_name == "ENM":
        args    = gen_top_ENM.get_option_script(sub)
        infile  = args.input
        outfile = args.output
        kENM    = args.kENM
        MAXdr   = args.maxr
        pspica  = args.pspica
        gen     = gen_top_ENM.gen_top_ENM(infile, outfile, kENM, MAXdr, pspica)
        gen.run()
    elif args.tool_name == "json2top":
        args  = json_to_top.get_option_script(sub)
        res   = args.resname
        top   = f"{res}.top"
        jfile = args.json
        da    = args.dupang
        jt    = json_to_top.json_to_top(jfile, da)
        jt.run(res, top)
    elif args.tool_name == "map2cg":
        args     = map_to_cg.get_option_script(sub)
        infile   = args.input
        outfile  = args.output
        jsonfile = args.json
        nodelwat = args.nodelwat
        verbose  = args.verbose
        mapCG    = map_to_cg.map_to_cg(infile, outfile, jsonfile, nodelwat, verbose)
        mapCG.run()
    elif args.tool_name == "maptraj":
        args     = map_traj.get_option_script(sub)
        inPDB    = args.inputPDB
        inTRAJ   = args.inputTRAJ
        outTRAJ  = args.outputTRAJ
        outPDB   = args.outpdb
        jsonfile = args.json
        nodelwat = args.nodelwat
        beg      = args.begin
        last     = args.last
        mt       = map_traj.map_traj(inPDB, inTRAJ, outTRAJ, outPDB, jsonfile, nodelwat, beg, last)
        mt.run()
    else:
        sys.exit("ERROR: invalid tool name.")
