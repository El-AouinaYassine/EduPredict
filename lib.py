def mult_mtx(m1 = [0][0] , m2= [0][0]):
    print(len(m1[0]))
    # res_mtx[][1]=[]
    for line in m1:
        return 0

mult_mtx(m1 = [[1,3],[2,3],[1,3]])

def predict(X , w , b):
    return X * w + b  
def mtx_predict(X, W , b=0):
    return np.matmul(X,W)

def mtx_loss(X, Y , w , b):
    return np.average((mtx_predict(X , w) - Y)**2)
def loss(X, Y , w , b):
    return np.average((predict(X, w , b) - Y)**2) 

def gradient(X , Y , w ,b=0):
    grad_w  =  2 * np.average(X * (predict(X,w,b)-Y) )
    grad_b =  2 * np.average((predict(X,w,b)-Y) )
    return grad_w ,grad_b

