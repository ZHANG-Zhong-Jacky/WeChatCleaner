import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='Clean or copy wechat files by month.')
parser.add_argument('-i',  action='store_true', help='apply to images')
parser.add_argument('-f', action='store_true', help='apply to files')
parser.add_argument('-t',  action='store_true', help='apply to thumbs')
parser.add_argument('-v',  action='store_true', help='apply to videos')
parser.add_argument('-a', action='store_true', default=True, help='apply to all')
parser.add_argument('-c', type=str, help='Copy destination, e.g. "C:\\Users\\someone\\Desktop"')
parser.add_argument('-d', action='store_true', help='delete corresponding files')
parser.add_argument('-l', action='store_true', help='show corresponding files')
parser.add_argument('-m',  type=str, help='the month to perform on, e.g. "2022-07"', required=True)
parser.add_argument('-r',  type=str, default='.',
    help='dir to MsgAttach, e.g. "C:\\Users\\yourname\\Documents\\WeChat Files\\wxid_dv3ivfuepz1p21\\FileStorage\\MsgAttach", default="."')

args = parser.parse_args()

if(args.i or args.f or args.t or args.v):
    args.a = False

if(args.a):
    args.i=args.f=args.t=args.v=True

total=[]

def calls(cmd):
    print (cmd)
    p = subprocess.Popen(['powershell.exe', cmd])
    p.communicate()


def work2(dr):
    for d in os.listdir(dr):
        path = os.path.join(dr,d)
        if (d==args.m):
            if (args.l):
                for p in os.listdir(path):
                    total.append(p)
            if (args.c):
                for p in os.listdir(path):
                    calls('cp -Force "'+os.path.join(path,p)+'" "'+args.c+'"')
            if (args.d):
                calls('rm -R -force "'+path+'"')
    if not os.listdir(dr):
        calls('rm -force "'+dr+'"')

def work(dr):
    for d in os.listdir(dr):
        path = os.path.join(dr,d)
        for c in os.listdir(path):
            if c == 'Image':
                if args.i:
                    work2(os.path.join(path,c))
            elif c == 'Thumb':
                if args.t:
                    work2(os.path.join(path,c))
            elif c == 'Video':
                if args.v:
                    work2(os.path.join(path,c))
            elif c == 'File':
                if args.f:
                    work2(os.path.join(path,c))
        if not os.listdir(path):
            calls('rm -force "'+path+'"')

if (args.c):
    calls('mkdir -Force "'+args.c+'"')

work(os.path.abspath(args.r))

if args.l:
    print(total)