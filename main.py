from classes import *


especiais=['\\','/',':','*','?','"','<','>','|',"'","..","SYS:"]
pointer=Folder("ponteiro")
root = Folder("SYS:")
root.address=root.name
pointer=root


def _lista_nomes(target):
    lista=[]
    for n in range(len(target.children)):
        lista.append(target.children[n].name)
    return lista

def _check_special(entry):
    immaculate=True
    for n in especiais:
        if n in entry:
            print("ERRO: O nome não pode conter '{}'".format(n))
            immaculate=False
            break
    if immaculate==False:        
        return False
    else:
        return True
    
def mkdir(diretorio):
    diretorio=diretorio.strip(" ")
    
    if diretorio=="":
        print("ERRO: Nome do diretorio não definido")
        return

    if diretorio in _lista_nomes(pointer):
        print("ERRO: Já existe arquivo ou pasta com esse nome")
        return

    if _check_special(diretorio):    
        new_folder = Folder(diretorio)
        new_folder.parent = pointer
        new_folder.address=new_folder.parent.address +"/"+ new_folder.name
        new_folder.parent.children.append(new_folder)
        print("Diretório criado")
    else:
        return

def ls():
    print("")
    for n in range(len(pointer.children)):
        if isinstance(pointer.children[n], File) == True:
            print("{}".format(pointer.children[n].name))
        else:
            print("{}/".format(pointer.children[n].name))
    
def _set_dir(diretorio,target):
    if diretorio=="\\" or diretorio=="/" or diretorio=="SYS:":
        return root
    elif diretorio=="..":
        return target.parent
    elif diretorio in _lista_nomes(target):
        if isinstance(target.children[_lista_nomes(target).index(diretorio)], Folder)==False:
            print("ERRO: Esse diretorio não é uma pasta")
            return "break"
        else:
            return target.children[_lista_nomes(target).index(diretorio)]
    else:
        print("ERRO: Diretório não encontrado")
        return "break"
    

def cd(diretorio,target):
    diretorio=diretorio.strip(" ")
    
    if diretorio=="\\" or diretorio=="/" or diretorio=="SYS:":
        return root   
    elif diretorio=="..":
        return pointer.parent
    
    splitted=diretorio.split("/")  
    
    if "" in splitted:
        splitted.remove("")
    
    for n in range(len(splitted)):
        if (splitted[n] == "SYS:" or splitted[n] == "\\" or splitted[n] =="/") and n!=0:
            print("ERRO: Não se pode usar {} no meio do diretório".format(splitted[n]))
            return pointer
        target=_set_dir(splitted[n],target)
        if target=="break":
            return pointer
    return target
    
def touch(file_nick):
    file_nick=file_nick.strip(" ")
    
    if file_nick=="":
        print("ERRO: Nome do arquivo não definido")
        return

    if file_nick in _lista_nomes(pointer):
        print("ERRO: Já existe arquivo ou pasta")
        return

    if _check_special(file_nick):
        new_file = File(file_nick)
        new_file.parent = pointer
        new_file.address=new_file.parent.address +"/"+ new_file.name
        new_file.parent.children.append(new_file)
        print("Arquivo criado")
    else:
        return

def _change_child_address(target):
    target.address=target.parent.address +"/"+ target.name
    if isinstance(target.children, list)==False:
        return
    elif len(target.children)>0:
        for n in range(len(target.children)):
                _change_child_address(target.children[n])        

def rename(data):
    if data.count('"')!=4:
        print("ERRO: Nomes não definidos corretamente")
        return
    data=data.strip(" ")
    splitted=data.split('"')
    
    for n in range(len(splitted)):
        splitted[n]=splitted[n].strip(" ")
    
    while '' in splitted:
        splitted.remove('')
    
    if len(splitted)!=2:
        print("ERRO: Nomes não definidos corretamente")
        return
    
    old_name = splitted[0]
    new_name = splitted[1]

    if _check_special(new_name):
        if new_name in _lista_nomes(pointer):
            print("ERRO: Já existe pasta ou arquivo com esse nome")
            return
        elif old_name in _lista_nomes(pointer):
            target=pointer.children[_lista_nomes(pointer).index(old_name)]
            target.name=new_name
            _change_child_address(target)
        else:
            print("ERRO: Alvo a renomear não encontrado")

def rm(target):
    target=target.strip(" ")
    if target in _lista_nomes(pointer):
        del pointer.children[_lista_nomes(pointer).index(target)]
    else:
        print("ERRO: Alvo não encontrado")
    ls()

def tree(base,level):
    tab="   "*level
    if isinstance(base, Folder):
        print(tab+base.name+"/")
    else:
        print(tab+base.name)
    
    if isinstance(base.children, list)==False or base.children==[]:
        return
    for n in range(len(base.children)):
        tree(base.children[n],level+1)

print("\nDigite 'help' para ver a lista de comandos",end='')

    
if __name__ == '__main__':
    while root:
        print("")
        entry = input("TMNL {}> ".format(pointer.address))
        entry=entry.strip(" ")

        if entry == 'exit':
            break

        elif entry[:5] == "mkdir":
            if entry=="mkdir" or entry[5] != " ":
                print("ERRO: Diretório não definido")
            else:
                mkdir(entry[6:])

        elif entry == "ls" :            
            ls()

        elif entry[:2] == "cd":            
            if entry=="cd\\" or entry=="cd/":
                pointer=root
            elif entry=="cd" or entry[2]!=" ":
                print("ERRO: Diretorio não definido")
            else:
                pointer=cd(entry[3:],pointer)

        elif entry[:5] == "touch":
            if entry=="touch" or entry[5] != " ":
                print("ERRO: Arquivo não definido")
            else:
                touch(entry[6:])

        elif entry[:6] == 'rename':
            if len(entry) < 7:
                print("ERRO: Arquivo a renomear não definido\n")
            elif entry[6] != " ":
                print("ERRO: Ao chamar a função 'rename', dê um espaço antes do nome do arquivo\n")
            elif entry:
                rename(entry[7:])        
        
        elif entry[:2] == "rm":
            if len(entry) < 4:
                print("ERRO: Alvo não selecionado")
            elif entry[2] != ' ':
                print("ERRO: Ao chamar a função 'rm', dê um espaço antes do alvo\n")
            else:
                rm(entry[3:])
                
        elif entry=="tree":
            print("")
            tree(pointer,0)
        
        elif entry == "help":
            print("\nexit   -- Fecha o programa\nmkdir  -- Cria uma nova pasta\nls     -- Lista o conteúdo do diretório atual\ncd     -- Troca de diretório\ntouch  -- Cria novo arquivo\nrename -- Troca o nome de um arquivo ou pasta\nrm     -- Exclui pasta ou arquivo do diretório atual\ntree   -- Exibe subpastas e arquivos do diretório atual\n")

        elif entry != '':
            print("ERRO: Comando não reconhecido")