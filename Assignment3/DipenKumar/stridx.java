import java.io.*;
import java.util.*;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class Counter{
    volatile int count=0;
}

class Data{
    String word;
    Node node;
    Node node_inv;
}

class Node{
    Node parent=null;
    Character key=null;
    Map<Character,Node> treeMap=new TreeMap<Character,Node>();
    LinkedList<Data> list=new LinkedList<Data>();
}

class Result{
    LinkedList<Data> list=new LinkedList<Data>();

    int size(){
        return list.size();
    }

    int remove(){
        Iterator<Data> iterator=list.iterator();
        int count=0;
        while (iterator.hasNext()){
            Data data=iterator.next();
            if(data.word!=null){
                Node node;
                data.word=null;

                node=data.node;
                data.node=null;
                node.list.remove(data);
                while((node.list.size()==0)&&(node.treeMap.size()==0)&&(node.parent!=null)){
                    node.parent.treeMap.remove(node.key);
                    node=node.parent;
                }

                node=data.node_inv;
                data.node_inv=null;
                node.list.remove(data);
                while((node.list.size()==0)&&(node.treeMap.size()==0)&&(node.parent!=null)){
                    node.parent.treeMap.remove(node.key);
                    node=node.parent;
                }

                count++;
            }
        }
        return count;
    }
}

class StringIndex{

    Node head=new Node();
    Node head_inv=new Node();

    int insert(String word){
        Data data=new Data();
        data.word=word;
        Node node;

        node=head;
        for(int i=0;i<word.length();i++){
            char ch=word.charAt(i);
            if(!node.treeMap.containsKey(ch)){
                Node temp=new Node();
                temp.parent=node;
                temp.key=ch;
                node.treeMap.put(ch,temp);
            }
            node=node.treeMap.get(ch);
        }
        int count=node.list.size();
        node.list.add(data);
        data.node=node;

        node=head_inv;
        for(int i=word.length()-1;i>-1;i--){
            char ch=word.charAt(i);
            if(!node.treeMap.containsKey(ch)){
                Node temp=new Node();
                temp.parent=node;
                temp.key=ch;
                node.treeMap.put(ch,temp);
            }
            node=node.treeMap.get(ch);
        }
        int count_inv=node.list.size();
        node.list.add(data);
        data.node_inv=node;

        return count;
    }

    void search(Node node,Result result){
        Iterator<Data> iterator=node.list.iterator();
        while (iterator.hasNext()){
            result.list.add(iterator.next());
        }
        for(Map.Entry<Character,Node> entry : node.treeMap.entrySet()){
            search(entry.getValue(),result);
        }
    }

    Result stringsWithPrefix(String prefix){
        Result result=new Result();
        Node node=head;
        for(int i=0;i<prefix.length();i++){
            char ch=prefix.charAt(i);
            if(!node.treeMap.containsKey(ch)){
                return result;
            }
            node=node.treeMap.get(ch);
        }
        search(node,result);
        return result;
    }

    Result stringsWithSuffix(String suffix){
        Result result=new Result();
        Node node=head_inv;
        for(int i=suffix.length()-1;i>-1;i--){
            char ch=suffix.charAt(i);
            if(!node.treeMap.containsKey(ch)){
                return result;
            }
            node=node.treeMap.get(ch);
        }
        search(node,result);
        return result;
    }

}

class Teller implements Runnable{

	StringIndex notebook;
	Map<String,Result> results;
	BufferedReader br;
	Lock lock,lock_read;
	Counter read,write;

	Teller(StringIndex notebook,Map<String,Result> results,BufferedReader br,Lock lock,Lock lock_read,Counter read,Counter write){
		this.notebook=notebook;
		this.results=results;
		this.br=br;
		this.lock=lock;
		this.lock_read=lock_read;
		this.read=read;
        this.write=write;
	}

	public void run(){
		try{
			while(true){
				lock.lock();
				String line=br.readLine();
				if(line==null){
					lock.unlock();
					break;
				}
				String[] tokens=line.split(" ");
				if(tokens[0].equals("Insert")){
					while((read.count!=0)||(write.count!=0)){

					}
					write.count++;
					lock.unlock();
                    String word;
                    if(tokens.length>1){
						word=tokens[1];
					}
                    else{
						word="";
					}
					System.out.println("Number of strings equivalent to \""+word+"\" prior to the new insertion is "+notebook.insert(word));
					write.count--;
				}
				else if(tokens[0].equals("StringsWithPrefix")){
					while(write.count!=0){

					}
                    lock_read.lock();
					read.count++;
                    lock_read.unlock();
					lock.unlock();
					String str=tokens[1];
					String prefix;
					if(tokens.length>2){
						prefix=tokens[2];
					}
					else{
						prefix="";
					}
					Result result=notebook.stringsWithPrefix(prefix);
					lock_read.lock();
                    read.count--;
					results.put(str,result);
					lock_read.unlock();
				}
				else if(tokens[0].equals("StringsWithSuffix")){
					while(write.count!=0){

					}
                    lock_read.lock();
					read.count++;
                    lock_read.unlock();
					lock.unlock();
					String str=tokens[1];
					String suffix;
					if(tokens.length>2){
						suffix=tokens[2];
					}
					else{
						suffix="";
					}
					Result result=notebook.stringsWithSuffix(suffix);
					lock_read.lock();
                    read.count--;
					results.put(str,result);
					lock_read.unlock();
				}
				else if(tokens[0].equals("Size")){
					lock.unlock();
                    String str=tokens[1];
					if(!results.containsKey(str)){
						System.out.println("No such Result exit for \""+str+"\"");
					}
					else {
						Result result=results.get(str);
						System.out.println("Number of strings in \""+str+"\" is "+result.size());
					}
				}
				else if(tokens[0].equals("Remove")){
					while((read.count!=0)||(write.count!=0)){

					}
					write.count++;
					lock.unlock();
					String str=tokens[1];
					if(!results.containsKey(str)){
						System.out.println("No such Result exit for \""+str+"\"");
					}
					else {
						Result result=results.get(str);
						System.out.println("Number of strings actually removed by \""+str+"\" is "+result.remove());
					}
				    write.count--;
				}
				else {
					lock.unlock();
					System.out.println("Query not supported for \""+tokens[0]+"\"");
				}
			}
		}
		catch(IOException e){
			e.printStackTrace();
		}
	}
}

class Driver {
    public static void main(String[] args) throws IOException, InterruptedException {
		StringIndex notebook=new StringIndex();
        Map<String,Result> results=new TreeMap<String,Result>();
		FileReader infile=new FileReader(args[0]);
		BufferedReader br=new BufferedReader(infile);
		Lock lock=new ReentrantLock();
		Lock lock_read=new ReentrantLock();
        Counter read=new Counter();
        Counter write=new Counter();
		Thread[] threads=new Thread[10];
		for(int i=0;i<10;i++) {
			threads[i]=new Thread(new Teller(notebook,results,br,lock,lock_read,read,write));
			threads[i].start();
		}
		for(int i=0;i<10;i++) {
			threads[i].join();
		}
		br.close();
	}
}
